import pytest
from typing import AsyncGenerator, Generator
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
import sys
from pathlib import Path

# Add the api directory to the Python path
api_path = str(Path(__file__).parent.parent)
if api_path not in sys.path:
    sys.path.append(api_path)

from main import app
from database import get_session
from assessments.models import Assessment, Question, Choice, ScoringMethod

# Use in-memory SQLite for testing
TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(name="engine")
def engine_fixture():
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)

@pytest.fixture
def session():
    from database import engine
    from sqlmodel import SQLModel, Session

    # Create all tables
    SQLModel.metadata.create_all(engine)

    # Create a new session for testing
    with Session(engine) as session:
        yield session

    # Drop all tables after test
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

@pytest.fixture(name="async_client")
async def async_client_fixture(session: Session) -> AsyncGenerator:
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
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
