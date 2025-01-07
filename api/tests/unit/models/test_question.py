from datetime import datetime, UTC
from assessments.models import Question

def test_question_creation():
    question = Question(
        text="Test Question",
        order=1,
        assessment_id=1
    )
    assert question.text == "Test Question"
    assert question.order == 1
    assert question.assessment_id == 1

def test_question_default_values():
    question = Question(
        text="Test Question",
        order=1,
        assessment_id=1
    )
    assert isinstance(question.created_at, datetime)
    assert question.created_at.tzinfo == UTC
    assert question.id is None  # Should be None until persisted 