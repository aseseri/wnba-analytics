# backend/tests/test_players_api.py
from fastapi.testclient import TestClient
from main import app

def test_create_and_get_player(db_session):
    with TestClient(app) as client:
        create_response = client.post(
            "/api/players",
            json={"first_name": "Caitlin", "last_name": "Clark", "team": "Indiana Fever"}
        )
        assert create_response.status_code == 200
        player_id = create_response.json()["id"]

        get_response = client.get(f"/api/players/{player_id}")
        assert get_response.status_code == 200
        assert get_response.json()["first_name"] == "Caitlin"

def test_get_nonexistent_player_returns_404(db_session):
    with TestClient(app) as client:
        response = client.get("/api/players/99999")
        assert response.status_code == 404

def test_add_and_get_stats_for_player(db_session):
    """Test adding stats to a player and verifying they are included in the response."""
    with TestClient(app) as client:
        # Step 1: Create a player
        player_res = client.post(
            "/api/players",
            json={"first_name": "Sabrina", "last_name": "Ionescu", "team": "New York Liberty"},
        )
        assert player_res.status_code == 200
        player_id = player_res.json()["id"]

        # Step 2: Add stats to that player
        stats_payload = {
            "season": "2024", "points_per_game": 19, "rebounds_per_game": 4, "assists_per_game": 7,
            "games_played": 30, "games_started": 30, "field_goal_percentage": 0.45,
            "three_point_percentage": 0.35, "steals_per_game": 1.5, "blocks_per_game": 0.8,
            "player_efficiency_rating": 22.5
        }
        stats_res = client.post(f"/api/players/{player_id}/stats", json=stats_payload)
        assert stats_res.status_code == 200

        # Step 3: Fetch the player and verify the stats are present
        response = client.get(f"/api/players/{player_id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data["stats"]) == 1
        assert data["stats"][0]["season"] == "2024"
        assert data["stats"][0]["points_per_game"] == 19
