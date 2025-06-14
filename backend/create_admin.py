# backend/create_admin.py
from database import SessionLocal, engine
from models import User, Base
from auth.security import get_password_hash

db = SessionLocal()
# Ensure the 'users' table exists
Base.metadata.create_all(bind=engine)

# Check if user already exists
if db.query(User).filter(User.username == "admin").first():
    print("Admin user already exists.")
else:
    # Create a new user with a hashed password
    hashed_password = get_password_hash("your_secret_password") # Choose a strong password
    admin_user = User(username="admin", hashed_password=hashed_password)
    db.add(admin_user)
    db.commit()
    print("Admin user created successfully.")

db.close()
