import pytest
from fastapi.testclient import TestClient
from users.models import User, Account
from users.enums import UserRole
from sqlmodel import Session


def test_create_user(client: TestClient, session: Session):
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
    response = client.post(
        "/users/",
        json={"email": sample_user.email, "password": "password123"},
    )
    assert response.status_code == 400


def test_read_users(client: TestClient, sample_user: User, session: Session):
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(user["email"] == sample_user.email for user in data)


def test_create_account(client: TestClient, sample_user: User, session: Session):
    response = client.post(
        "/accounts/",
        params={"user_id": sample_user.id},
        json={
            "first_name": "John",
            "last_name": "Doe",
            "role": UserRole.ASSESSMENT_DEVELOPER.value
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"
    assert data["role"] == UserRole.ASSESSMENT_DEVELOPER.value


def test_read_accounts(client: TestClient, sample_account: Account, session: Session):
    response = client.get("/accounts/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(account["first_name"] ==
               sample_account.first_name for account in data)
