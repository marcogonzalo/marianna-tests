import pytest
from users.schemas import UserCreate, UserRead, AccountCreate, AccountRead
from users.enums import UserRole

def test_user_create_validation():
    # Valid user
    user = UserCreate(
        email="test@example.com",
        password="password123"
    )
    assert user.email == "test@example.com"
    assert user.password == "password123"

    # Invalid email
    with pytest.raises(ValueError):
        UserCreate(
            email="invalid_email",
            password="password123"
        )

def test_account_create_validation():
    # Valid account
    account = AccountCreate(
        first_name="John",
        last_name="Doe",
        role=UserRole.ASSESSMENT_DEVELOPER
    )
    assert account.first_name == "John"
    assert account.last_name == "Doe"
    assert account.role == UserRole.ASSESSMENT_DEVELOPER

    # Empty first name
    with pytest.raises(ValueError):
        AccountCreate(
            first_name="",
            last_name="Doe",
            role=UserRole.ASSESSMENT_DEVELOPER
        )
