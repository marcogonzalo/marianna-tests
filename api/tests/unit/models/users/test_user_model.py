from datetime import date, datetime
from app.users.schemas import ExamineeCreate, ExamineeUpdate
from app.users.models import Examinee, User, Account
from app.users.enums import Gender, UserRole
from sqlmodel import Session
from app.utils.password import get_password_hash, verify_password


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


def test_account_creation(session: Session, sample_user_only: User):
    account = Account(
        user_id=sample_user_only.id,
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


def test_examinee_creation(session: Session, sample_user: User):
    examinee_data = ExamineeCreate(
        first_name="John",
        last_name="Doe",
        birth_date=date(2000, 1, 1),
        gender=Gender.MALE,
        email="john.doe@example.com",
        internal_identifier="ID123",
        comments="Test examinee",
        created_by=sample_user.account.id
    )
    examinee = Examinee(**examinee_data.model_dump())
    session.add(examinee)
    session.commit()
    session.refresh(examinee)

    assert examinee.id is not None
    assert examinee.first_name == "John"
    assert examinee.last_name == "Doe"


def test_examinee_update(session: Session, sample_user: User):
    examinee_data = ExamineeCreate(
        first_name="Jane",
        last_name="Doe",
        birth_date=date(2000, 1, 1),
        gender=Gender.FEMALE,
        email="jane.doe@example.com",
        internal_identifier="ID124",
        comments="Test examinee",
        created_by=sample_user.account.id
    )
    examinee = Examinee(**examinee_data.model_dump())
    session.add(examinee)
    session.commit()
    session.refresh(examinee)

    update_data = ExamineeUpdate(
        first_name="Janet",
        last_name="Doe",
        birth_date=date(2000, 1, 1),
        gender=Gender.FEMALE,
        email="jane.doe@example.com",
        internal_identifier="ID124",
        comments="Test examinee",
        created_by=sample_user.account.id
    )
    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(examinee, key, value)
    session.commit()
    session.refresh(examinee)

    assert examinee.first_name == "Janet"


def test_examinee_deletion(session: Session, sample_user: User):
    examinee_data = ExamineeCreate(
        first_name="Mark",
        last_name="Smith",
        birth_date=date(1998, 5, 15),
        gender=Gender.MALE,
        email="mark.smith@example.com",
        internal_identifier="ID125",
        comments="Test examinee",
        created_by=sample_user.account.id
    )
    examinee = Examinee(**examinee_data.model_dump())
    session.add(examinee)
    session.commit()
    session.refresh(examinee)

    session.delete(examinee)
    session.commit()

    deleted_examinee = session.query(Examinee).filter(
        Examinee.id == examinee.id).first()
    assert deleted_examinee is None
