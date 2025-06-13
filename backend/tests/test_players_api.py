# backend/tests/test_players_api.py
from fastapi.testclient import TestClient
from main import app

# Each test asks for the `db_session` fixture to ensure the database is clean.
def test_create_and_get_player(db_session):
    client = TestClient(app) # Create a client for this test
    create_response = client.post("/api/players", json={"first_name": "Caitlin", "last_name": "Clark", "team": "Indiana Fever"})
    assert create_response.status_code == 200
    player_id = create_response.json()["id"]

    get_response = client.get(f"/api/players/{player_id}")
    assert get_response.status_code == 200
    assert get_response.json()["first_name"] == "Caitlin"

def test_get_nonexistent_player_returns_404(db_session):
    client = TestClient(app)
    response = client.get("/api/players/99999")
    assert response.status_code == 404

def test_add_and_get_stats_for_player(db_session):
    client = TestClient(app)
    player_res = client.post("/api/players", json={"first_name": "Sabrina", "last_name": "Ionescu", "team": "New York Liberty"})
    player_id = player_res.json()["id"]
    stats_payload = {
        "season": "2024", "points_per_game": 19, "rebounds_per_game": 4, "assists_per_game": 7,
        "games_played": 30, "games_started": 30, "field_goal_percentage": 0.45,
        "three_point_percentage": 0.35, "steals_per_game": 1.5, "blocks_per_game": 0.8,
        "player_efficiency_rating": 22.5
    }
    stats_res = client.post(f"/api/players/{player_id}/stats", json=stats_payload)
    assert stats_res.status_code == 200
