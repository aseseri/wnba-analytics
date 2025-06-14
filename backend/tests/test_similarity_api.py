# backend/tests/test_similarity_api.py
from fastapi.testclient import TestClient
from unittest.mock import patch
import pandas as pd
import numpy as np
from main import app, get_db
import models
from auth.security import get_password_hash

def test_get_similar_players(db_session):
    mock_player_vectors = pd.DataFrame(index=['Player A (2024)', 'Player C (2024)'])
    mock_matrix = np.array([[1.0, 0.95], [0.95, 1.0]])

    with patch('main.joblib.load') as mock_joblib_load:
        mock_joblib_load.side_effect = [mock_player_vectors, mock_matrix]

        with TestClient(app) as client:
            # Create user, log in, get headers
            db = client.app.dependency_overrides[get_db]().__next__()
            user = models.User(username="testuser", hashed_password=get_password_hash("password"))
            db.add(user)
            db.commit()
            login_res = client.post("/auth/token", data={"username": "testuser", "password": "password"})
            token = login_res.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
            db.close()

            player_res = client.post("/api/players", headers=headers, json={"first_name": "Player", "last_name": "A", "team": "Team A"})
            assert player_res.status_code == 200
            player_id = player_res.json()["id"]

            # Call the similarity endpoint
            response = client.get(f"/api/players/{player_id}/seasons/2024/similar")

            assert response.status_code == 200
            data = response.json()
            assert data[0]["player_season_id"] == "Player C (2024)"