from datetime import datetime
from users.models import User, Account
from users.enums import UserRole
from sqlmodel import Session
from users.utils import get_password_hash, verify_password

def test_user_creation(session: Session):
    user = User(
        email="test@example.com",
        password_hash=get_password_hash("hashedpassword123")
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    assert user.email == "test@example.com"
    assert verify_password("hashedpassword123", user.password_hash)
    assert isinstance(user.created_at, datetime)
    assert user.id is not None
    # assert user.created_at.tzinfo is not None
    # assert user.created_at.tzinfo == timezone.utc

def test_account_creation(session: Session, sample_user: User):
    account = Account(
        user_id=sample_user.id,
        first_name="John",
        last_name="Doe",
        role=UserRole.ASSESSMENT_DEVELOPER.value
    )
    session.add(account)
    session.commit()
    session.refresh(account)

    assert account.first_name == "John"
    assert account.last_name == "Doe"
    assert account.role == UserRole.ASSESSMENT_DEVELOPER.value
    assert isinstance(account.created_at, datetime)
#     assert account.created_at.tzinfo == timezone.utc
#     assert account.user_id == sample_user.id
