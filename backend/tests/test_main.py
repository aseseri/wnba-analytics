# backend/tests/test_main.py

def test_read_root(test_client):
    """
    Tests if the root API endpoint ('/api') returns a successful response
    and the expected JSON message.
    """
    response = test_client.get("/api")
    assert response.status_code == 200
    assert response.json() == {"message": "WNBA Analytics API is running!"}
