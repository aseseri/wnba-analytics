# backend/tests/test_main.py
from fastapi.testclient import TestClient
from main import app

# This test doesn't need a database, so it doesn't need a fixture.
def test_read_root():
    # It creates its own client.
    client = TestClient(app)
    response = client.get("/api")
    assert response.status_code == 200
    assert response.json() == {"message": "WNBA Analytics API is running!"}
