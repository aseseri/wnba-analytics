# backend/tests/test_players_api.py

def test_create_player_as_authenticated_user(authenticated_client):
    """Tests that a logged-in user can create a player."""
    response = authenticated_client.post(
        "/api/players",
        json={"first_name": "Caitlin", "last_name": "Clark", "team": "Indiana Fever"}
    )
    assert response.status_code == 200
    assert response.json()["first_name"] == "Caitlin"

def test_create_player_unauthenticated(test_client):
    """Tests that a non-logged-in user cannot create a player."""
    response = test_client.post(
        "/api/players",
        json={"first_name": "Caitlin", "last_name": "Clark", "team": "Indiana Fever"}
    )
    assert response.status_code == 401 # Unauthorized