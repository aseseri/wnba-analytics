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

def test_add_stats_to_player(db_session):
    """
    Test adding stats to an existing player.
    """
    # First, create a player to add stats to
    player_response = client.post(
        "/api/players",
        json={"first_name": "Aliyah", "last_name": "Boston", "team": "Indiana Fever"}
    )
    player_id = player_response.json()["id"]

    # Now, add stats to that player
    stats_response = client.post(
        f"/api/players/{player_id}/stats",
        json={"season": "2023", "points_per_game": 14, "rebounds_per_game": 8, "assists_per_game": 2}
    )
    assert stats_response.status_code == 200, stats_response.text
    stats_data = stats_response.json()
    assert stats_data["season"] == "2023"

    # Verify that the player now has these stats
    response = client.get(f"/api/players/{player_id}")
    player_data = response.json()
    assert len(player_data["stats"]) == 1
    assert player_data["stats"][0]["points_per_game"] == 14