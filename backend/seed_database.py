# backend/seed_database.py
import json
import logging
from database import SessionLocal, engine
from models import Player, PlayerStat, Base

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# List the JSON files you generated with your scraper
DATA_FILES = [
    'data/wnba_combined_2024.json'
]

def seed_data():
    db = SessionLocal()
    logger.info("Database connection established.")

    try:
        # Clear old data for a fresh start
        num_stats_deleted = db.query(PlayerStat).delete()
        num_players_deleted = db.query(Player).delete()
        db.commit()
        logger.info(f"Cleared old data: {num_players_deleted} players and {num_stats_deleted} stats records deleted.")

        all_players = {} # A dictionary to keep track of players we've added

        for file_name in DATA_FILES:
            year = file_name.split('_')[2].split('.')[0] # Extract year from filename
            logger.info(f"Processing data for {year} from {file_name}...")

            with open(file_name, 'r') as f:
                data = json.load(f)

            for player_data in data:
                player_name = player_data.get("Player")
                team = player_data.get("Team")

                if not player_name or not team:
                    continue

                # Check if we've already created this player
                if player_name not in all_players:
                    # Handle cases where a player played for multiple teams (e.g., 'TOT' for total)
                    # We'll take the first team we see for simplicity
                    if team == 'TOT':
                       # Find the first real team abbreviation for that player in the dataset
                       real_team_row = next((p for p in data if p.get('Player') == player_name and p.get('Team') != 'TOT'), None)
                       if real_team_row:
                           team = real_team_row.get('Team')
                       else:
                           continue # Skip if we can't find a real team

                    first_name, *last_name_parts = player_name.split(' ')
                    last_name = ' '.join(last_name_parts)

                    new_player = Player(
                        first_name=first_name,
                        last_name=last_name,
                        team=team
                    )
                    db.add(new_player)
                    db.commit()
                    db.refresh(new_player)
                    all_players[player_name] = new_player.id
                    logger.info(f"Created player: {player_name}")

                # Create the stat line for this player and season
                # Note: We are using the per-game stats if available, otherwise totals.
                # Your JSON has both, e.g., 'PTS' (total) and 'PTS' per game is usually calculated.
                # Let's assume your JSON provides total points and games played ('G')
                games_played = player_data.get('G', 1)
                if games_played == 0: games_played = 1 # Avoid division by zero

                new_stat = PlayerStat(
                    player_id=all_players[player_name],
                    season=year,

                    # -- Basic Per-Game Stats --
                    points_per_game=round(player_data.get('PTS', 0) / games_played, 1),
                    rebounds_per_game=round(player_data.get('TRB', 0) / games_played, 1),
                    assists_per_game=round(player_data.get('AST', 0) / games_played, 1),

                    # -- Add the richer data --
                    games_played=player_data.get('G', 0),
                    games_started=player_data.get('GS', 0),
                    field_goal_percentage=player_data.get('FG%', 0.0),
                    three_point_percentage=player_data.get('3P%', 0.0),
                    steals_per_game=round(player_data.get('STL', 0) / games_played, 1),
                    blocks_per_game=round(player_data.get('BLK', 0) / games_played, 1),
                    player_efficiency_rating=player_data.get('PER', 0.0)
                )
                db.add(new_stat)

        db.commit()
        logger.info("Successfully seeded database from JSON files.")

    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        db.rollback()
    finally:
        db.close()
        logger.info("Database session closed.")

if __name__ == "__main__":
    logger.info("Starting database seeding process...")
    Base.metadata.create_all(bind=engine)
    seed_data()
