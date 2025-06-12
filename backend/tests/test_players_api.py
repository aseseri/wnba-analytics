# backend/test_players_api.py
from fastapi.testclient import TestClient
from main import app, get_db
from database import Base, engine
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# --- Test Database Setup ---
# Use a separate in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the tables in the test database
Base.metadata.create_all(bind=engine)

# This is a pytest "fixture" - it runs before each test that needs it
@pytest.fixture(scope="function")
def db_session():
    """Create a new database session for a test."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# This overrides the get_db dependency in your app for the duration of the tests
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

# --- Actual Tests ---
def test_create_and_get_player(db_session):
    """
    Test creating a player and then retrieving them.
    """
    # Create a player
    response = client.post(
        "/api/players",
        json={"first_name": "Caitlin", "last_name": "Clark", "team": "Indiana Fever"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["first_name"] == "Caitlin"
    assert "id" in data
    player_id = data["id"]

    # Get the player
    response = client.get(f"/api/players/{player_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["first_name"] == "Caitlin"

def test_get_single_player_with_stats(db_session):
    """
    Tests that we can retrieve a single player by their ID and that
    their stats are included and correctly structured.
    """
    # Step 1: Create a player to test with
    player_res = client.post(
        "/api/players",
        json={"first_name": "Sabrina", "last_name": "Ionescu", "team": "New York Liberty"},
    )
    assert player_res.status_code == 200
    player_id = player_res.json()["id"]

    # Step 2: Add stats to that player
    stats_res = client.post(
        f"/api/players/{player_id}/stats",
        json={
            "season": "2024",
            "points_per_game": 19,
            "rebounds_per_game": 4,
            "assists_per_game": 7,
            "games_played": 30,
            "games_started": 30,
            "field_goal_percentage": 0.45,
            "three_point_percentage": 0.35,
            "steals_per_game": 1.5,
            "blocks_per_game": 0.8,
            "player_efficiency_rating": 22.5
        }
    )
    # The assertion will now pass because the data is valid
    assert stats_res.status_code == 200

    # Step 3: Fetch the single player and verify their details and stats
    response = client.get(f"/api/players/{player_id}")
    assert response.status_code == 200
    data = response.json()

    # Assertions for player details
    assert data["first_name"] == "Sabrina"
    assert data["id"] == player_id

    # Assertions for the nested stats data
    assert "stats" in data
    assert isinstance(data["stats"], list)
    assert len(data["stats"]) == 1
    assert data["stats"][0]["season"] == "2024"
    assert data["stats"][0]["points_per_game"] == 19

def test_get_nonexistent_player_returns_404(db_session):
    """
    Tests that requesting a player ID that doesn't exist returns a 404 Not Found error.
    """
    response = client.get("/api/players/99999") # Use an ID that is unlikely to exist
    assert response.status_code == 404
    assert response.json()["detail"] == "Player not found"
