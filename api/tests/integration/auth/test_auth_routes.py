import pytest
from fastapi.testclient import TestClient
from jose import jwt
from sqlmodel import Session
from app.auth.services import SECRET_KEY, ALGORITHM
from app.users.models import User
from app.utils.password import get_password_hash


@pytest.fixture
def auth_user(session: Session) -> User:
    user = User(
        email="auth_test@example.com",
        password_hash=get_password_hash("testpassword123")
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def test_login_success(client: TestClient, auth_user: User):
    response = client.post(
        "/auth/token",
        data={
            "username": auth_user.email,
            "password": "testpassword123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["email"] == "auth_test@example.com"

    # Verify token is valid
    token = data["access_token"]
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["sub"] == "auth_test@example.com"


def test_login_invalid_credentials(client: TestClient, auth_user: User):
    response = client.post(
        "/auth/token",
        data={
            "username": auth_user.email,
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"


def test_logout(client: TestClient, auth_user: User):
    # First login to get token
    login_response = client.post(
        "/auth/token",
        data={
            "username": auth_user.email,
            "password": "testpassword123"
        }
    )
    token = login_response.json()["access_token"]

    # Test logout
    response = client.post(
        "/auth/logout",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Successfully logged out"

    # Verify token is blacklisted by trying to use it
    protected_response = client.get(
        "/users/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert protected_response.status_code == 401


def test_refresh_token(client: TestClient, auth_user: User):
    # First login to get initial tokens
    login_response = client.post(
        "/auth/token",
        data={
            "username": auth_user.email,
            "password": "testpassword123"
        }
    )
    token = login_response.json()["access_token"]

    # Create a valid refresh token
    from datetime import timedelta
    from app.auth.services import AuthService
    refresh_token = AuthService.create_access_token(
        {"sub": auth_user.email},
        expires_delta=timedelta(days=7)
    )

    # Test token refresh
    response = client.post(
        "/auth/refresh",
        json={"refresh_token": refresh_token}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    assert data["email"] == "auth_test@example.com"

    # Verify new token is valid
    new_token = data["access_token"]
    payload = jwt.decode(new_token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["sub"] == "auth_test@example.com"


def test_refresh_token_invalid(client: TestClient):
    response = client.post(
        "/auth/refresh",
        json={"refresh_token": "invalid_token"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid refresh token"
