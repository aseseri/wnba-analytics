# backend/build_similarity_model.py

import logging
import pandas as pd
import joblib
import json

from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# The JSON files are now the source of truth for the build
DATA_FILES = [
    'wnba_combined_2024.json',
    'wnba_combined_2023.json',
    'wnba_combined_2022.json' 
]

def build_model():
    logger.info("Loading player data from JSON files...")

    all_seasons_df = []
    for file_name in DATA_FILES:
        year = file_name.split('_')[2].split('.')[0]
        with open(file_name, 'r') as f:
            season_data = json.load(f)

            # Add a 'season' column to each record
            for record in season_data:
                record['season'] = year

            all_seasons_df.append(pd.DataFrame(season_data))

    df = pd.concat(all_seasons_df, ignore_index=True)

    # Clean player names and handle multi-team players ('TOT')
    df['Player'] = df['Player'].str.replace('*', '', regex=False)
    df = df[df['Team'] != 'TOT'] # Exclude total rows
    df = df.dropna(subset=['Player']) # Drop rows with no player name

    logger.info(f"Successfully loaded {len(df)} total player seasons.")

    # Define the unique ID and the features for the model
    df['player_season_id'] = df['Player'] + ' (' + df['season'] + ')'
    features = [
        'PTS', 'TRB', 'AST', 'STL', 'BLK', 'FG%', '3P%', 'PER', 'WS'
    ]
    # Ensure all feature columns exist and fill NaNs with 0
    for feature in features:
        if feature not in df.columns:
            df[feature] = 0
    df[features] = df[features].fillna(0)

    df_features = df.set_index('player_season_id')[features]

    # Normalize the data
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(df_features)
    logger.info("Features have been scaled.")

    # Calculate Cosine Similarity
    similarity_matrix = cosine_similarity(scaled_features)
    logger.info("Similarity matrix has been calculated.")

    # Save the artifacts
    joblib.dump(df_features, 'similarity_data.joblib')
    joblib.dump(similarity_matrix, 'similarity_matrix.joblib')

    logger.info("Model artifacts have been saved successfully!")

if __name__ == "__main__":
    build_model()