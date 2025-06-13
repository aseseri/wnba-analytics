# backend/tests/test_similarity_api.py
from fastapi.testclient import TestClient
from unittest.mock import patch
import pandas as pd
import numpy as np
import pytest
from main import app

# This test also asks for `db_session` to ensure the database is clean.
def test_get_similar_players(db_session):
    mock_player_vectors = pd.DataFrame(
        {'pts': [0.9, -0.5, 0.85], 'reb': [0.8, -0.6, 0.9]},
        index=['Player A (2024)', 'Player B (2024)', 'Player C (2024)']
    )
    mock_matrix = np.array([[1.0, 0.1, 0.95], [0.1, 1.0, 0.2], [0.95, 0.2, 1.0]])

    # 1. We set up the mock using 'with patch'
    with patch('main.joblib.load') as mock_joblib_load:
        def side_effect(filename):
            if "data" in filename: return mock_player_vectors
            if "matrix" in filename: return mock_matrix
        mock_joblib_load.side_effect = side_effect

        # 2. We create the TestClient INSIDE the patch block.
        # This is the critical part that forces the app's startup
        # event to run while our mock is active.
        with TestClient(app) as client:
            # 3. Setup the DB with a player
            player_res = client.post("/api/players", json={"first_name": "Player", "last_name": "A", "team": "Team A"})
            assert player_res.status_code == 200
            player_id = player_res.json()["id"]

            # 4. Call the API endpoint
            response = client.get(f"/api/players/{player_id}/seasons/2024/similar")

            # 5. Assert the response
            assert response.status_code == 200
            data = response.json()
            assert data[0]["player_season_id"] == "Player C (2024)"
