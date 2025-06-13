# backend/tests/test_main.py
from fastapi.testclient import TestClient
from main import app

def test_read_root():
    # The 'with' statement ensures the app's lifespan events run
    with TestClient(app) as client:
        response = client.get("/api")
        assert response.status_code == 200
        assert response.json() == {"message": "WNBA Analytics API is running!"}
