# backend/main.py
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from contextlib import asynccontextmanager # Lifespan manager
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict
from typing import List

import joblib
import pandas as pd
import numpy as np

# Import your SQLAlchemy models and session management
import models
import database

# This (lifespan) function will run when the application starts
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup: creating database tables...")
    database.Base.metadata.create_all(bind=database.engine)
    yield
    print("Application shutdown.")

app = FastAPI(lifespan=lifespan)

origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get a database session for each request
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Pydantic Schemas ---
class PlayerStatBase(BaseModel):
    season: str
    points_per_game: float
    rebounds_per_game: float
    assists_per_game: float
    games_played: int
    games_started: int
    field_goal_percentage: float
    three_point_percentage: float
    steals_per_game: float
    blocks_per_game: float
    player_efficiency_rating: float

class PlayerStatCreate(PlayerStatBase):
    pass

class PlayerStat(PlayerStatBase):
    id: int
    player_id: int
    model_config = ConfigDict(from_attributes=True)

class PlayerBase(BaseModel):
    first_name: str
    last_name: str
    team: str

class PlayerCreate(PlayerBase):
    pass

class Player(PlayerBase):
    id: int
    stats: List[PlayerStat] = []
    model_config = ConfigDict(from_attributes=True)

# ---- API ENDPOINTS ----
@app.get("/api")
def read_root():
    return {"message": "WNBA Analytics API is running!"}

# Endpoint to CREATE a new player
@app.post("/api/players", response_model=Player)
def create_player(player: PlayerCreate, db: Session = Depends(get_db)):
    new_player = models.Player(**player.model_dump())
    db.add(new_player)
    db.commit()
    db.refresh(new_player)
    return new_player

# Endpoint to READ all players
@app.get("/api/players", response_model=List[Player])
def get_players(db: Session = Depends(get_db)):
    players = db.query(models.Player).all()
    return players

@app.get("/api/players/{player_id}", response_model=Player)
def get_player(player_id: int, db: Session = Depends(get_db)):
    player = db.query(models.Player).filter(models.Player.id == player_id).first()
    if player is None: raise HTTPException(status_code=404, detail="Player not found")
    return player

# Endpoint to DELETE a player
@app.delete("/api/players/{player_id}")
def delete_player(player_id: int, db: Session = Depends(get_db)):
    player_to_delete = db.query(models.Player).filter(models.Player.id == player_id).first()
    if player_to_delete is None: raise HTTPException(status_code=404, detail="Player not found")
    db.delete(player_to_delete)
    db.commit()
    return {"message": "Player deleted successfully"}

# Endpoint to UPDATE a player
@app.put("/api/players/{player_id}", response_model=Player)
def update_player(player_id: int, player_update: PlayerCreate, db: Session = Depends(get_db)):
    player_to_update = db.query(models.Player).filter(models.Player.id == player_id).first()
    if player_to_update is None: raise HTTPException(status_code=404, detail="Player not found")

    # Update the player's attributes
    for key, value in player_update.model_dump().items():
        setattr(player_to_update, key, value)

    db.commit()
    db.refresh(player_to_update)
    return player_to_update

@app.post("/api/players/{player_id}/stats", response_model=PlayerStat)
def create_stats_for_player(player_id: int, stat: PlayerStatCreate, 
                            db: Session = Depends(get_db)):
    db_player = db.query(models.Player).filter(models.Player.id == player_id).first()
    if db_player is None: raise HTTPException(status_code=404, detail="Player not found")
    db_stat = models.PlayerStat(**stat.model_dump(), player_id=player_id)
    db.add(db_stat)
    db.commit()
    db.refresh(db_stat)
    return db_stat

# Load the ML artifacts when the application starts (once at startup for efficiency)
try:
    similarity_df = joblib.load("similarity_data.joblib")
    similarity_matrix = joblib.load("similarity_matrix.joblib")
    logger.info("Similarity model artifacts loaded successfully.")
except FileNotFoundError:
    similarity_df = None
    similarity_matrix = None
    logger.warning("Similarity model artifacts not found. Run build_similarity_model.py.")

# A Pydantic schema for the similarity response
class SimilarPlayer(BaseModel):
    player_season_id: str
    similarity_score: float

# The Similarity API Endpoint
@app.get("/api/players/{player_id}/seasons/{season}/similar", response_model=List[SimilarPlayer])
def get_similar_players(player_id: int, season: str, db: Session = Depends(get_db)):
    if similarity_df is None: raise HTTPException(status_code=503, detail="Similarity model is not available.")

    # Find the player to get their name
    player = db.query(models.Player).filter(models.Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    # Construct the ID used in our similarity model
    player_season_id = f"{player.first_name} {player.last_name} ({season})"

    try:
        # Get the index of our target player in the similarity matrix
        target_idx = similarity_df.index.get_loc(player_season_id)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Stats for {player_season_id} not found in model.")

    # Get the similarity scores for this player against all others
    similarity_scores = list(enumerate(similarity_matrix[target_idx]))

    # Sort the players by similarity score in descending order
    sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    # Get the top 6 scores (the first one will be the player themselves, so we skip it)
    top_similar_indices = [i[0] for i in sorted_scores[1:6]]
    top_similar_scores = [i[1] for i in sorted_scores[1:6]]

    # Get the names of the similar players
    similar_players_names = similarity_df.index[top_similar_indices].tolist()

    # Format the response
    response = [
        {"player_season_id": name, "similarity_score": score}
        for name, score in zip(similar_players_names, top_similar_scores)
    ]

    return response
