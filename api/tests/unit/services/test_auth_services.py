import pytest
from datetime import datetime, timedelta
from jose import jwt
from app.auth.services import AuthService, SECRET_KEY, ALGORITHM
from app.users.models import User
from app.utils.password import get_password_hash


def test_create_access_token():
    data = {"sub": "test@example.com"}
    expires_delta = timedelta(minutes=15)
    token = AuthService.create_access_token(data, expires_delta)

    # Verify token can be decoded and contains expected data
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["sub"] == "test@example.com"
    assert "exp" in payload


def test_authenticate_user(session):
    # Create a test user
    user = User(
        email="test@example.com",
        password_hash=get_password_hash("testpassword")
    )
    session.add(user)
    session.commit()

    # Test valid authentication
    authenticated_user = AuthService.authenticate_user(
        session, "test@example.com", "testpassword"
    )
    assert authenticated_user is not None
    assert authenticated_user['email'] == "test@example.com"

    # Test invalid password
    invalid_user = AuthService.authenticate_user(
        session, "test@example.com", "wrongpassword"
    )
    assert invalid_user is None

    # Test non-existent user
    nonexistent_user = AuthService.authenticate_user(
        session, "nonexistent@example.com", "testpassword"
    )
    assert nonexistent_user is None


def test_token_blacklisting(session):
    # Create a test token
    test_token = "test_token"
    expires_at = datetime.utcnow() + timedelta(minutes=15)

    # Blacklist the token
    AuthService.blacklist_token(session, test_token, expires_at)

    # Verify token is blacklisted
    assert AuthService.is_token_blacklisted(session, test_token) is True

    # Verify non-blacklisted token
    assert AuthService.is_token_blacklisted(session, "other_token") is False


def test_clean_expired_tokens(session):
    # Create expired token
    expired_token = "expired_token"
    expired_at = datetime.utcnow() - timedelta(minutes=15)
    AuthService.blacklist_token(session, expired_token, expired_at)

    # Create valid token
    valid_token = "valid_token"
    valid_until = datetime.utcnow() + timedelta(minutes=15)
    AuthService.blacklist_token(session, valid_token, valid_until)

    # Clean expired tokens
    AuthService.clean_expired_tokens(session)

    # Verify expired token was removed and valid token remains
    assert AuthService.is_token_blacklisted(session, expired_token) is False
    assert AuthService.is_token_blacklisted(session, valid_token) is True
