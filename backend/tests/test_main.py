# backend/tests/test_main.py

def test_read_root(test_client):
    """Tests the public root API endpoint."""
    response = test_client.get("/api")
    assert response.status_code == 200
    assert response.json() == {"message": "WNBA Analytics API is running!"}

def test_get_players_publicly(test_client):
    """Tests that anyone can view the list of players."""
    response = test_client.get("/api/players")
    assert response.status_code == 200