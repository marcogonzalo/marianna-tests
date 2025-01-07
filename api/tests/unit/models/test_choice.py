from datetime import datetime, UTC
from assessments.models import Choice

def test_choice_creation():
    choice = Choice(
        text="Test Choice",
        value=1.0,
        order=1,
        question_id=1
    )
    assert choice.text == "Test Choice"
    assert choice.value == 1.0
    assert choice.order == 1
    assert choice.question_id == 1

def test_choice_default_values():
    choice = Choice(
        text="Test Choice",
        value=1.0,
        order=1,
        question_id=1
    )
    assert isinstance(choice.created_at, datetime)
    assert choice.created_at.tzinfo == UTC
    assert choice.id is None  # Should be None until persisted 