# backend/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# --- Check for a test-specific database URL first ---
# The getenv() function reads an environment variable.
# We provide a default value for local development.
# DATABASE_URL = os.getenv(
#     "DATABASE_URL", 
#     "postgresql://admin:password123@db/wnba_db"
# )
# This function will now build the database URL based on the environment
def get_database_url():
    # Check if we are running in the Google Cloud Run environment
    if os.getenv("K_SERVICE"):
        db_user = os.environ["DB_USER"]
        db_pass = os.environ["DB_PASS"]
        db_name = os.environ["DB_NAME"]
        db_socket_dir = "/cloudsql"
        instance_connection_name = os.environ["INSTANCE_CONNECTION_NAME"]

        # --- THIS IS THE CORRECTED URL FORMAT ---
        # It uses a query parameter `?host=` for the socket path.
        return (
            f"postgresql+psycopg2://{db_user}:{db_pass}@/{db_name}"
            f"?host={db_socket_dir}/{instance_connection_name}"
        )
    else:
        # This is for local development and remains unchanged
        return "postgresql://admin:password123@db:5432/wnba_db"
    
DATABASE_URL = get_database_url()

# --- Use the DATABASE_URL variable ---
engine = create_engine(DATABASE_URL)

# # For SQLite, we need a special argument. We'll add it only if needed.
# if "sqlite" in DATABASE_URL:
#     engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()