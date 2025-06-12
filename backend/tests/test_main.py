# backend/test_main.py
from fastapi.testclient import TestClient
from main import app # Import your FastAPI app

# Create a TestClient instance
client = TestClient(app)

def test_read_root():
    """
    Tests if the root API endpoint ('/api') returns a successful response
    and the expected JSON message.
    """
    # Make a simulated request to your API
    response = client.get("/api")

    # Assert that the status code is 200 (OK)
    assert response.status_code == 200

    # Assert that the response body is what you expect
    assert response.json() == {"message": "WNBA Analytics API is running!"}