# backend/tests/conftest.py
import pytest
import os

# This tells our app to use the SQLite DB for all tests.
os.environ['DATABASE_URL'] = "sqlite:///./test.db"

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app, get_db
from database import Base, engine # We can now import the engine safely

# Create the test-specific database engine
engine = create_engine(
    os.environ['DATABASE_URL'],
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency to use the test database
app.dependency_overrides[get_db] = lambda: TestingSessionLocal()

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestingSessionLocal()
    del app.dependency_overrides[get_db]
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def test_client(db_session):
    yield TestClient(app)
