import pytest
from datetime import datetime, UTC
from assessments.models import Question, Choice, Assessment, ScoringMethod

def test_question_creation(session):
    # Create an assessment first
    assessment = Assessment(
        title="Test Assessment",
        scoring_method=ScoringMethod.BOOLEAN,
        min_value=0,
        max_value=1
    )
    session.add(assessment)
    session.commit()

    question = Question(
        text="Test Question",
        order=1,
        assessment_id=assessment.id
    )
    assert question.text == "Test Question"
    assert question.order == 1
    assert question.assessment_id == assessment.id

def test_question_default_values(session):
    # Create an assessment first
    assessment = Assessment(
        title="Test Assessment",
        scoring_method=ScoringMethod.BOOLEAN,
        min_value=0,
        max_value=1
    )
    session.add(assessment)
    session.commit()

    question = Question(
        text="Test Question",
        order=1,
        assessment_id=assessment.id
    )
    assert isinstance(question.created_at, datetime)
    assert question.created_at.tzinfo == UTC
    assert question.id is None  # Should be None until persisted

def test_question_alter_choice_list(session):
    # Create an assessment first
    assessment = Assessment(
        title="Test Assessment",
        description="Test Description",
        scoring_method=ScoringMethod.BOOLEAN,
        min_value=0,
        max_value=1
    )
    session.add(assessment)
    session.commit()

    # Create question
    question = Question(
        text="Test Question",
        order=1,
        assessment_id=assessment.id  # Use the actual assessment id
    )
    session.add(question)
    session.commit()

    # Create choices using data that mimics ChoiceCreate schema
    from assessments.schemas import ChoiceCreate
    choices = [
        ChoiceCreate(text="Choice 1", value=1.0, order=1),
        ChoiceCreate(text="Choice 2", value=0.0, order=2)
    ]

    # Call alter_choice_list with the choice data
    question.alter_choice_list(choices, session)
    session.commit()
    session.refresh(question)

    assert len(question.choices) == 2
    assert question.choices[0].text == "Choice 1"
    assert question.choices[1].text == "Choice 2"

def test_question_update_attributes():
    from pydantic import BaseModel

    class QuestionUpdateData(BaseModel):
        text: str
        order: int

    question = Question(
        text="Original Text",
        order=1,
        assessment_id=1
    )

    update_data = QuestionUpdateData(text="Updated Text", order=2)
    question.update_attributes(update_data)

    assert question.text == "Updated Text"
    assert question.order == 2
