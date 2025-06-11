# backend/main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel # Import Pydantic

# Import your SQLAlchemy models and session management
import models
import database

# This creates the database tables
# It will check if the "players" table exists, and if not, it will create it
database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

origins = [
    "http://localhost:3000",
]

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

# Pydantic model for creating a player (data validation)
class PlayerCreate(BaseModel):
    first_name: str
    last_name: str
    team: str

# ---- API ENDPOINTS ----

@app.get("/api")
def read_root():
    return {"message": "WNBA Analytics API is running!"}

# Endpoint to CREATE a new player
@app.post("/api/players")
def create_player(player: PlayerCreate, db: Session = Depends(get_db)):
    new_player = models.Player(
        first_name=player.first_name,
        last_name=player.last_name,
        team=player.team
    )
    db.add(new_player)
    db.commit()
    db.refresh(new_player)
    return new_player

# Endpoint to READ all players
@app.get("/api/players")
def get_players(db: Session = Depends(get_db)):
    players = db.query(models.Player).all()
    return players