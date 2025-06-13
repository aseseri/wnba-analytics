# backend/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# --- Check for a test-specific database URL first ---
# The getenv() function reads an environment variable.
# We provide a default value for local development.
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://admin:password123@db/wnba_db"
)

# --- Use the DATABASE_URL variable ---
engine = create_engine(DATABASE_URL)

# For SQLite, we need a special argument. We'll add it only if needed.
if "sqlite" in DATABASE_URL:
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()