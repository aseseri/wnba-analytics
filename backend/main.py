# backend/main.py
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from contextlib import asynccontextmanager # Lifespan manager
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict
from typing import List, Annotated

import joblib
import pandas as pd
import numpy as np

# Import your SQLAlchemy models and session management
import models
import database
from database import get_db
from auth.router import router as auth_router # Import our new auth router
from auth.router import get_current_user # Import our new dependency

# --- The Lifespan function now loads the model ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup...")

    # Load the ML artifacts and attach them to the app's state
    try:
        app.state.similarity_df = joblib.load("similarity_data.joblib")
        app.state.similarity_matrix = joblib.load("similarity_matrix.joblib")
        logger.info("Similarity model artifacts loaded successfully.")
    except FileNotFoundError:
        app.state.similarity_df = None
        app.state.similarity_matrix = None
        logger.warning("Similarity model artifacts not found. Run build_similarity_model.py.")

    # This part is for the database tables
    database.Base.metadata.create_all(bind=database.engine)

    yield # The application runs here

    logger.info("Application shutdown.")

app = FastAPI(lifespan=lifespan)
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])

origins = [
    "http://localhost:3000",
    "https://wnba-frontend-service-776933261932.us-west1.run.app"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

class UserOut(BaseModel):
    id: int
    username: str
    model_config = ConfigDict(from_attributes=True)

# ---- PROTECTED API ENDPOINTS ----
# Endpoint to CREATE a new player
@app.post("/api/players", response_model=Player)
def create_player(player: PlayerCreate, current_user: Annotated[models.User, Depends(get_current_user)], db: Session = Depends(get_db)):
    new_player = models.Player(**player.model_dump())
    db.add(new_player)
    db.commit()
    db.refresh(new_player)
    return new_player

# Endpoint to UPDATE a player 
@app.put("/api/players/{player_id}", response_model=Player)
def update_player(player_id: int, player_update: PlayerCreate, current_user: Annotated[models.User, Depends(get_current_user)], db: Session = Depends(get_db)):
    player_to_update = db.query(models.Player).filter(models.Player.id == player_id).first()
    if player_to_update is None: raise HTTPException(status_code=404, detail="Player not found")

    # Update the player's attributes
    for key, value in player_update.model_dump().items():
        setattr(player_to_update, key, value)

    db.commit()
    db.refresh(player_to_update)
    return player_to_update

# Endpoint to DELETE a player
@app.delete("/api/players/{player_id}")
def delete_player(player_id: int, current_user: Annotated[models.User, Depends(get_current_user)], db: Session = Depends(get_db)):
    player_to_delete = db.query(models.Player).filter(models.Player.id == player_id).first()
    if player_to_delete is None: raise HTTPException(status_code=404, detail="Player not found")
    db.delete(player_to_delete)
    db.commit()
    return {"message": "Player deleted successfully"}  
    
@app.post("/api/players/{player_id}/stats", response_model=PlayerStat)
def create_stats_for_player(player_id: int, stat: PlayerStatCreate, current_user: Annotated[models.User, Depends(get_current_user)], db: Session = Depends(get_db)):
    db_player = db.query(models.Player).filter(models.Player.id == player_id).first()
    if db_player is None: raise HTTPException(status_code=404, detail="Player not found")
    db_stat = models.PlayerStat(**stat.model_dump(), player_id=player_id)
    db.add(db_stat)
    db.commit()
    db.refresh(db_stat)
    return db_stat

@app.get("/users", response_model=List[UserOut])
def read_users(current_user: Annotated[models.User, Depends(get_current_user)], db: Session = Depends(get_db)):
    """
    Retrieves a list of all users.
    This is a protected endpoint that requires authentication.
    The `response_model` ensures that only the fields from `UserOut` (id, username)
    are returned, protecting the hashed password.
    """
    users = db.query(models.User).all()
    return users

# ---- PUBLIC API ENDPOINTS ----
@app.get("/api")
def read_root():
    return {"message": "WNBA Analytics API is running!"}

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

# A Pydantic schema for the similarity response
class SimilarPlayer(BaseModel):
    player_season_id: str
    similarity_score: float

# The Similarity API Endpoint
@app.get("/api/players/{player_id}/seasons/{season}/similar", response_model=List[SimilarPlayer])
def get_similar_players(player_id: int, season: str, request: Request, db: Session = Depends(get_db)):
    # Get the loaded models from the application state
    similarity_df = request.app.state.similarity_df
    similarity_matrix = request.app.state.similarity_matrix

    if similarity_df is None:
        raise HTTPException(status_code=503, detail="Similarity model is not available.")

    player = db.query(models.Player).filter(models.Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    player_season_id = f"{player.first_name} {player.last_name} ({season})"

    try:
        target_idx = similarity_df.index.get_loc(player_season_id)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Stats for {player_season_id} not found in model.")

    similarity_scores = list(enumerate(similarity_matrix[target_idx]))
    sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    top_similar_indices = [i[0] for i in sorted_scores[1:6]]
    top_similar_scores = [i[1] for i in sorted_scores[1:6]]
    similar_players_names = similarity_df.index[top_similar_indices].tolist()

    response = [
        {"player_season_id": name, "similarity_score": score}
        for name, score in zip(similar_players_names, top_similar_scores)
    ]

    return response
