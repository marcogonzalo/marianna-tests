import pytest
import sys
from fastapi.testclient import TestClient
from datetime import date, timedelta
from typing import AsyncGenerator, Generator
from httpx import AsyncClient, ASGITransport
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from pathlib import Path
from database import get_session
from main import app

from app.utils.datetime import get_current_datetime
from app.utils.password import get_password_hash
from app.assessments.models import Assessment, Choice, Question, ScoringMethod
from app.responses.models import AssessmentResponse, QuestionResponse
from app.users.enums import Gender
from app.users.models import Examinee, User, Account

# Add the api directory to the Python path
api_path = str(Path(__file__).parent.parent)
if api_path not in sys.path:
    sys.path.append(api_path)


# Use in-memory SQLite for testing
TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(name="engine", scope="function")
def engine_fixture():
    """Create a new engine for each test."""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="session")
def session_fixture(engine):
    """Create a new database session for each test."""
    # Create a new session with the test engine
    session = Session(engine)

    try:
        yield session
    finally:
        # Ensure proper cleanup of the session
        session.close()
        # Clear any uncommitted changes
        session.rollback()


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Create a new FastAPI TestClient with session override."""
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="async_client")
async def async_client_fixture(session: Session) -> AsyncGenerator:
    """Create a new AsyncClient for async tests."""
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client
    app.dependency_overrides.clear()

# Test data fixtures


@pytest.fixture
def sample_assessment(session: Session):
    assessment = Assessment(
        title="Test Assessment",
        description="Test Description",
        scoring_method=ScoringMethod.BOOLEAN,
        min_value=0,
        max_value=1
    )
    session.add(assessment)
    session.commit()
    session.refresh(assessment)
    return assessment


@pytest.fixture(name="sample_question")
def sample_question_fixture(session: Session, sample_assessment: Assessment) -> Question:
    question = Question(
        text="Test Question",
        order=1,
        assessment_id=sample_assessment.id
    )
    session.add(question)
    session.commit()
    session.refresh(question)
    return question


@pytest.fixture(name="sample_choice")
def sample_choice_fixture(session: Session, sample_question: Question) -> Choice:
    choice = Choice(
        text="Test Choice",
        value=1,
        order=1,
        question_id=sample_question.id
    )
    session.add(choice)
    session.commit()
    session.refresh(choice)
    return choice


@pytest.fixture
def sample_user(session: Session) -> User:
    user = User(
        email="test@example.com",
        password_hash=get_password_hash("hashedpassword123")
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture
def sample_admin_user(session: Session) -> User:
    user = User(
        email="admin@example.com",
        password_hash=get_password_hash("hashedpassword123")
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture
def sample_account(session: Session, sample_user: User) -> Account:
    from app.users.models import Account
    from app.users.enums import UserRole

    account = Account(
        user_id=sample_user.id,
        first_name="John",
        last_name="Doe",
        role=UserRole.ASSESSMENT_DEVELOPER
    )
    session.add(account)
    session.commit()
    session.refresh(account)
    return account



@pytest.fixture
def sample_admin_account(session: Session, sample_admin_user: User) -> Account:
    from app.users.models import Account
    from app.users.enums import UserRole

    account = Account(
        user_id=sample_admin_user.id,
        first_name="Admin",
        last_name="Doe",
        role=UserRole.ADMIN
    )
    session.add(account)
    session.commit()
    session.refresh(account)
    return account


@pytest.fixture
def sample_examinee(session: Session, sample_account: Account) -> Examinee:
    user = Examinee(
        first_name="Marianna",
        last_name="Rolo",
        email="test@example.com",
        birth_date=date(2000, 1, 1),
        gender=Gender.FEMALE,
        created_by=sample_account.id
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture
def sample_assessment_response(session: Session, sample_assessment: Assessment, sample_examinee: Examinee, sample_account: Account):
    # Create a sample AssessmentResponse
    assessment_response = AssessmentResponse(
        assessment_id=sample_assessment.id,
        examinee_id=sample_examinee.id,
        status="pending",
        created_at=get_current_datetime(),
        updated_at=get_current_datetime(),
        created_by=sample_account.id
    )
    session.add(assessment_response)
    session.commit()
    session.refresh(assessment_response)
    return assessment_response


@pytest.fixture
def sample_question_response(session: Session, sample_assessment_response: AssessmentResponse):
    # Create a sample QuestionResponse
    question_response = QuestionResponse(
        assessment_response_id=sample_assessment_response.id,
        question_id=1,  # Assuming a question with ID 1 exists
        numeric_value=5.0,
        text_value="Sample answer",
        created_at=get_current_datetime()
    )
    session.add(question_response)
    session.commit()
    session.refresh(question_response)
    return question_response


@pytest.fixture
def auth_token(sample_user: User) -> str:
    from app.auth.services import AuthService
    access_token = AuthService.create_access_token(
        data={"sub": sample_user.email},
        expires_delta=timedelta(minutes=30)
    )
    return access_token

@pytest.fixture
def auth_token_admin(session: Session, sample_admin_user: User, sample_admin_account: Account) -> str:
    from app.auth.services import AuthService
    sample_admin_account.user = sample_admin_user
    session.add(sample_admin_account)
    session.commit()
    session.refresh(sample_admin_account)
    access_token = AuthService.create_access_token(
        data={"sub": sample_admin_user.email},
        expires_delta=timedelta(minutes=30)
    )
    return access_token


@pytest.fixture
def auth_headers(auth_token: str) -> dict:
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture
def auth_headers_admin(auth_token_admin: str) -> dict:
    return {"Authorization": f"Bearer {auth_token_admin}"}
