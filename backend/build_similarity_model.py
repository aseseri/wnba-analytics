# backend/build_similarity_model.py
import logging
import pandas as pd
import joblib
from sqlalchemy import text
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity

from database import SessionLocal, engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def build_model():
    logger.info("Connecting to database to fetch player stats...")
    db = SessionLocal()

    # Load all player stats into a Pandas DataFrame
    # SQL query to join players and stats
    query = """
    SELECT
        p.id as player_id,
        p.first_name,
        p.last_name,
        ps.season,
        ps.points_per_game,
        ps.rebounds_per_game,
        ps.assists_per_game,
        ps.steals_per_game,
        ps.blocks_per_game,
        ps.field_goal_percentage,
        ps.three_point_percentage,
        ps.player_efficiency_rating
    FROM players p
    JOIN player_stats ps ON p.id = ps.player_id
    """
    df = pd.read_sql(text(query), con=engine.connect())
    db.close()
    logger.info(f"Successfully loaded {len(df)} player seasons from the database.")

    if df.empty:
        logger.error("No data found in the database. Please run the seed script first.")
        return

    # Select features used for comparison
    features = [
        'points_per_game', 'rebounds_per_game', 'assists_per_game',
        'steals_per_game', 'blocks_per_game', 'field_goal_percentage',
        'three_point_percentage', 'player_efficiency_rating'
    ]

    # Unique identifier for each player-season
    df['player_season_id'] = df['first_name'] + ' ' + df['last_name'] + ' (' + df['season'] + ')'
    df_features = df.set_index('player_season_id')[features]

    # Normalize the data
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(df_features)
    logger.info("Features have been scaled.")

    # Calculate Cosine Similarity
    # This creates a big matrix where every player-season is compared to every other one.
    # The result is a score from 0 (completely different) to 1 (identical).
    similarity_matrix = cosine_similarity(scaled_features)
    logger.info("Similarity matrix has been calculated.")

    # Save the artifacts
    joblib.dump(df_features, 'similarity_data.joblib')
    joblib.dump(similarity_matrix, 'similarity_matrix.joblib')

    logger.info("Model artifacts have been saved successfully!")
    logger.info("-> similarity_data.joblib (Player data and vectors)")
    logger.info("-> similarity_matrix.joblib (Comparison scores)")


if __name__ == "__main__":
    build_model()