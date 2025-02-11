import pytest
from assessments.schemas import (
    AssessmentCreate,
    QuestionCreate,
    ChoiceCreate,
    AssessmentResponseCreate
)
from assessments.models import ScoringMethod, ResponseStatus

def test_assessment_create_validation():
    # Valid assessment with boolean scoring
    assessment = AssessmentCreate(
        title="Test Assessment",
        scoring_method=ScoringMethod.BOOLEAN
    )
    assert assessment.title == "Test Assessment"
    assert assessment.scoring_method == ScoringMethod.BOOLEAN

    # Invalid custom scoring (missing min/max values)
    with pytest.raises(ValueError, match="Custom scoring method requires explicit min_value and max_value"):
        AssessmentCreate(
            title="Test Assessment",
            scoring_method=ScoringMethod.CUSTOM,
            min_value=None,
            max_value=None
        )

    # Valid custom scoring
    assessment = AssessmentCreate(
        title="Test Assessment",
        scoring_method=ScoringMethod.CUSTOM,
        min_value=0.0,
        max_value=10.0
    )
    assert assessment.min_value == 0.0
    assert assessment.max_value == 10.0

def test_choice_create_validation():
    # Valid choice
    choice = ChoiceCreate(
        text="Test Choice",
        value=1.0,
        order=1
    )
    assert choice.text == "Test Choice"
    assert choice.value == 1.0

    # Invalid empty text
    with pytest.raises(ValueError):
        ChoiceCreate(
            text="",
            value=1.0,
            order=1
        )

def test_question_create_validation():
    # Valid question with choices
    question = QuestionCreate(
        text="Test Question",
        order=1,
        choices=[
            ChoiceCreate(text="Choice 1", value=1.0, order=1),
            ChoiceCreate(text="Choice 2", value=0.0, order=2)
        ]
    )
    assert question.text == "Test Question"
    assert len(question.choices) == 2

    # Invalid question without choices
    with pytest.raises(ValueError):
        QuestionCreate(
            text="Test Question",
            order=1,
            choices=[]
        )
