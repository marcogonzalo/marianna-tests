import pytest
from typing import AsyncGenerator, Generator
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
import sys
from pathlib import Path

from users.utils import get_password_hash
from assessments.models import Assessment, Choice, Question, ScoringMethod
from users.models import User, Account

# Add the api directory to the Python path
api_path = str(Path(__file__).parent.parent)
if api_path not in sys.path:
    sys.path.append(api_path)

from main import app
from database import get_session

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
def sample_account(session: Session, sample_user: User) -> Account:
    from users.models import Account
    from users.enums import UserRole

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
