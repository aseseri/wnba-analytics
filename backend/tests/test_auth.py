# backend/tests/test_auth.py
from auth.security import get_password_hash
import models
from database import SessionLocal

def test_login_for_access_token(test_client):
    """Tests if a user can successfully log in with correct credentials."""
    # Setup: Create a user directly in the test database
    db = SessionLocal()
    password = "correct_password"
    user = models.User(username="logintestuser", hashed_password=get_password_hash(password))
    db.add(user)
    db.commit()
    db.close()

    # Execute & Assert
    response = test_client.post(
        "/auth/token",
        data={"username": "logintestuser", "password": "correct_password"}
    )
    assert response.status_code == 200, response.text
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_with_wrong_password(test_client):
    """Tests that login fails with an incorrect password."""
    db = SessionLocal()
    user = models.User(username="wrongpassuser", hashed_password=get_password_hash("correct_password"))
    db.add(user)
    db.commit()
    db.close()

    response = test_client.post(
        "/auth/token",
        data={"username": "wrongpassuser", "password": "incorrect_password"}
    )
    assert response.status_code == 401 # Unauthorized

def test_read_users_as_authenticated_user(authenticated_client):
    """
    Tests that a logged-in user can successfully fetch the list of users.
    """
    # The authenticated_client fixture has already created and logged in a "testuser"
    response = authenticated_client.get("/users")

    # Assert success
    assert response.status_code == 200
    data = response.json()

    # Assert the response format is correct
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["username"] == "testuser"

    # CRITICAL: Assert that the hashed password is NOT present
    assert "hashed_password" not in data[0]

def test_read_users_unauthenticated(test_client):
    """
    Tests that a non-logged-in user receives a 401 error when trying
    to access the protected user list.
    """
    # We use the basic, unauthenticated client here
    response = test_client.get("/users")
    assert response.status_code == 401 # Unauthorized   