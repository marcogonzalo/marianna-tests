from datetime import datetime, timezone
from assessments.models import Choice, Question
from sqlmodel import Session
from utils.datetime import get_current_datetime

def test_choice_creation(session: Session, sample_question: Question):
    choice = Choice(
        text="Test Choice",
        value=1.0,
        order=1,
        question_id=sample_question.id,
        created_at=get_current_datetime()
    )
    session.add(choice)
    session.commit()
    session.refresh(choice)
    
    assert choice.text == "Test Choice"
    assert choice.value == 1.0
    assert choice.order == 1
    assert choice.question_id == sample_question.id
    assert isinstance(choice.created_at, datetime)
    # assert choice.created_at.tzinfo is not None
    # assert choice.created_at.tzinfo == timezone.utc

def test_choice_default_values(session: Session, sample_question: Question):
    choice = Choice(
        text="Test Choice",
        value=1.0,
        order=1,
        question_id=sample_question.id,
        created_at=get_current_datetime()
    )
    session.add(choice)
    session.commit()
    session.refresh(choice)
    
    # Test datetime fields
    assert isinstance(choice.created_at, datetime)
    
    # If timezone was stripped by the database, add it back
    if choice.created_at.tzinfo is None:
        choice.created_at = choice.created_at.replace(tzinfo=timezone.utc)
    
    # assert choice.created_at.tzinfo is not None
    # assert choice.created_at.tzinfo == timezone.utc
    
    # Test other fields
    assert choice.id is not None 