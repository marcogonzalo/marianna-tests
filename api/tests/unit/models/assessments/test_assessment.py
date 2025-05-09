import pytest
from datetime import datetime
from app.assessments.models import Assessment, ScoringMethod
from sqlmodel import Session


def test_assessment_creation(session: Session):
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

    assert assessment.title == "Test Assessment"
    assert assessment.description == "Test Description"
    assert assessment.scoring_method == ScoringMethod.BOOLEAN
    assert assessment.min_value == 0
    assert assessment.max_value == 1
    # assert assessment.created_at.tzinfo is not None
    # assert assessment.created_at.tzinfo == timezone.utc


def test_assessment_default_values(session: Session):
    assessment = Assessment(
        title="Test Assessment",
        scoring_method=ScoringMethod.BOOLEAN,
        min_value=0,
        max_value=1
    )
    session.add(assessment)
    session.commit()
    session.refresh(assessment)

    assert assessment.description is None
    assert isinstance(assessment.created_at, datetime)
    assert isinstance(assessment.updated_at, datetime)
    # assert assessment.created_at.tzinfo is not None
    # assert assessment.created_at.tzinfo == timezone.utc
    # assert assessment.updated_at.tzinfo is not None
    # assert assessment.updated_at.tzinfo == timezone.utc


def test_set_default_values_boolean():
    assessment = Assessment(
        title="Test Assessment",
        scoring_method=ScoringMethod.BOOLEAN,
        min_value=0,
        max_value=0  # Invalid values that should be corrected
    )
    assessment.set_default_values()
    assert assessment.min_value == 0
    assert assessment.max_value == 1


def test_set_default_values_scored():
    assessment = Assessment(
        title="Test Assessment",
        scoring_method=ScoringMethod.SCORED,
        min_value=0,
        max_value=0  # Invalid values that should be corrected
    )
    assessment.set_default_values()
    assert assessment.min_value == -1
    assert assessment.max_value == 1


def test_set_default_values_custom():
    assessment = Assessment(
        title="Test Assessment",
        scoring_method=ScoringMethod.CUSTOM,
        min_value=0,
        max_value=0
    )
    with pytest.raises(ValueError, match="Custom scoring method requires explicit min_value and max_value"):
        assessment.set_default_values()


def test_assessment_relationships(session: Session):
    assessment = Assessment(
        title="Test Assessment",
        scoring_method=ScoringMethod.BOOLEAN,
        min_value=0,
        max_value=1
    )
    session.add(assessment)
    session.commit()
    session.refresh(assessment)

    assert hasattr(assessment, 'questions')
    assert hasattr(assessment, 'responses')
    assert isinstance(assessment.questions, list)
    assert isinstance(assessment.responses, list)


def test_assessment_invalid_custom_scoring():
    assessment = Assessment(
        title="Test Assessment",
        scoring_method=ScoringMethod.CUSTOM,
        min_value=None,  # Invalid for CUSTOM
        max_value=None   # Invalid for CUSTOM
    )
    with pytest.raises(ValueError):
        assessment.set_default_values()
