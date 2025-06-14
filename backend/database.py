# backend/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

def get_database_url():
    """
    Gets the database URL from environment variables with a specific order of priority:
    1. An explicit DATABASE_URL (used for testing).
    2. Google Cloud Run's special socket connection (for production).
    3. The local Docker PostgreSQL database (for development).
    """
    # 1. Highest priority: Check for the testing URL.
    if db_url := os.getenv("DATABASE_URL"):
        return db_url

    # 2. Second priority: Check if running in Google Cloud Run.
    if os.getenv("K_SERVICE"):
        db_user = os.environ["DB_USER"]
        db_pass = os.environ["DB_PASS"]
        db_name = os.environ["DB_NAME"]
        db_socket_dir = "/cloudsql"
        instance_connection_name = os.environ["INSTANCE_CONNECTION_NAME"]

        # Return the Unix Socket connection string.
        return (
            f"postgresql+psycopg2://{db_user}:{db_pass}@/{db_name}"
            f"?host={db_socket_dir}/{instance_connection_name}"
        )

    # 3. Default: Fall back to the local Docker database URL.
    return "postgresql://admin:password123@db:5432/wnba_db"
    
DATABASE_URL = get_database_url()
connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Dependency to get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
