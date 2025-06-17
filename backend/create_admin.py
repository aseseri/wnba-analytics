# backend/create_admin.py
import os
from database import SessionLocal, engine
from models import User, Base
from auth.security import get_password_hash
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ADMIN_USERNAME = os.getenv("ADMIN_USER", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

def create_admin_user():
    if not ADMIN_PASSWORD:
        logger.error("ADMIN_PASSWORD environment variable not set. Cannot create admin user.")
        return

    db = SessionLocal()
    Base.metadata.create_all(bind=engine)   # Ensure the 'users' table exists

    # Check if user already exists
    if db.query(User).filter(User.username == ADMIN_USERNAME).first():
        logger.warning(f"Admin user '{ADMIN_USERNAME}' already exists.")
    else:
        # Create a new user with a hashed password
        hashed_password = get_password_hash(ADMIN_PASSWORD)
        admin_user = User(username=ADMIN_USERNAME, hashed_password=hashed_password)
        db.add(admin_user)
        db.commit()
        logger.info(f"Admin user '{ADMIN_USERNAME}' created successfully.")

    db.close()

if __name__ == "__main__":
    create_admin_user()
