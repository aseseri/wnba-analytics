# backend/tests/test_similarity_api.py
from fastapi.testclient import TestClient
from unittest.mock import patch
import pandas as pd
import numpy as np
import pytest
from main import app

def test_get_similar_players(db_session):
    """
    Tests the similarity endpoint correctly by using the TestClient as a
    context manager, which triggers the lifespan event.
    """
    mock_player_vectors = pd.DataFrame(
        {'pts': [0.9, -0.5, 0.85], 'reb': [0.8, -0.6, 0.9]},
        index=['Player A (2024)', 'Player B (2024)', 'Player C (2024)']
    )
    mock_matrix = np.array([
        [1.0, 0.1, 0.95],
        [0.1, 1.0, 0.2],
        [0.95, 0.2, 1.0]
    ])

    # We patch joblib.load for the duration of the test
    with patch('main.joblib.load') as mock_joblib_load:
        def side_effect(filename):
            if "data" in filename: return mock_player_vectors
            if "matrix" in filename: return mock_matrix
        mock_joblib_load.side_effect = side_effect

        # The 'with' statement here is the critical fix. It ensures the
        # app's lifespan event runs, which calls joblib.load, which our
        # patch then intercepts.
        with TestClient(app) as client:
            # Setup the database with a test player
            player_res = client.post("/api/players", json={"first_name": "Player", "last_name": "A", "team": "Team A"})
            assert player_res.status_code == 200
            player_id = player_res.json()["id"]

            # Call the API endpoint
            response = client.get(f"/api/players/{player_id}/seasons/2024/similar")

            # Assert the response
            assert response.status_code == 200
            data = response.json()
            assert data[0]["player_season_id"] == "Player C (2024)"
            assert data[0]["similarity_score"] == pytest.approx(0.95)
