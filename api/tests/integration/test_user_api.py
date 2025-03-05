import pytest
from fastapi.testclient import TestClient
from app.users.models import User, Account
from app.users.enums import UserRole
from sqlmodel import Session
from datetime import timedelta
from app.auth.services import AuthService


@pytest.fixture
def auth_token(sample_user: User) -> str:
    access_token = AuthService.create_access_token(
        data={"sub": sample_user.email},
        expires_delta=timedelta(minutes=30)
    )
    return access_token


@pytest.fixture
def auth_headers(auth_token: str) -> dict:
    return {"Authorization": f"Bearer {auth_token}"}


def test_create_user(client: TestClient, session: Session):
    # Creating user doesn't require authentication
    response = client.post(
        "/users/",
        json={"email": "test@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_create_duplicate_user(client: TestClient, sample_user: User, session: Session):
    # Creating user doesn't require authentication
    response = client.post(
        "/users/",
        json={"email": sample_user.email, "password": "password123"},
    )
    assert response.status_code == 400


def test_read_users(client: TestClient, sample_user: User, auth_headers: dict, session: Session):
    response = client.get("/users/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(user["email"] == sample_user.email for user in data)


def test_create_account(client: TestClient, sample_user: User, auth_headers: dict, session: Session):
    response = client.post(
        "/accounts/",
        params={"user_id": sample_user.id},
        json={
            "first_name": "John",
            "last_name": "Doe",
            "role": UserRole.ASSESSMENT_DEVELOPER.value
        },
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"
    assert data["role"] == UserRole.ASSESSMENT_DEVELOPER.value


def test_read_accounts(client: TestClient, sample_account: Account, auth_headers: dict, session: Session):
    response = client.get("/accounts/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(account["first_name"] ==
               sample_account.first_name for account in data)
