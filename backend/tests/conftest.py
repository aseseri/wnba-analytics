# backend/tests/conftest.py
import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Set the environment variable BEFORE other imports.
os.environ['DATABASE_URL'] = "sqlite:///./test.db"

from main import app, get_db
from database import Base, engine

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """
    This fixture creates a clean database with all tables for a single test function,
    and then drops all tables after the test is done.
    """
    Base.metadata.create_all(bind=engine)

    # This is the key: we override the app's dependency to use our
    # clean, temporary database for the duration of the test.
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    # Yield nothing, just perform setup and teardown
    yield

    # Teardown: clean up the override and drop tables
    del app.dependency_overrides[get_db]
    Base.metadata.drop_all(bind=engine)
