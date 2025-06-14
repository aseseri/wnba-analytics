# backend/tests/conftest.py
import pytest
import os

# This MUST be the first thing to run. It configures the app for testing.
os.environ['DATABASE_URL'] = "sqlite:///./test.db"

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app, get_db
from database import Base, engine
from auth.security import get_password_hash
import models

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """
    The single fixture to provide a clean database session for each test.
    It creates all tables before the test and drops them all after.
    This guarantees perfect test isolation.
    """
    # --- SETUP ---
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    # Override the dependency for the duration of the test
    app.dependency_overrides[get_db] = override_get_db

    yield

    # --- TEARDOWN ---
    del app.dependency_overrides[get_db]
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def test_client():
    """
    Provides a TestClient with a clean database for each test.
    Handles startup/shutdown events and DB table creation/destruction.
    """
    # --- SETUP ---
    Base.metadata.create_all(bind=engine)
    
    def override_get_db():
        """This function overrides the production database dependency."""
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client
    
    # --- TEARDOWN ---
    # Clean up after the test is done
    del app.dependency_overrides[get_db]
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def authenticated_client(test_client):
    """
    Provides an authenticated TestClient. It uses the regular test_client
    and performs a login to get an auth token.
    """
    # We need a direct session to create the user in the database first
    db = TestingSessionLocal()
    password = "testpassword"
    
    # Create user if it doesn't exist to avoid IntegrityError
    user = db.query(models.User).filter(models.User.username == "testuser").first()
    if not user:
        user = models.User(username="testuser", hashed_password=get_password_hash(password))
        db.add(user)
        db.commit()
    
    db.close()
    
    # Log in as the test user to get a token
    login_response = test_client.post(
        "/auth/token",
        data={"username": "testuser", "password": password}
    )
    assert login_response.status_code == 200, "Failed to log in during test setup"
    token = login_response.json()["access_token"]
    
    # Set the auth header for all future requests with this client
    test_client.headers["Authorization"] = f"Bearer {token}"
    
    return test_client