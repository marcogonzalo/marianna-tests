import pytest
from datetime import datetime, UTC
from assessments.models import Assessment, ScoringMethod

def test_assessment_creation():
    assessment = Assessment(
        title="Test Assessment",
        description="Test Description",
        scoring_method=ScoringMethod.BOOLEAN,
        min_value=0,
        max_value=1
    )
    assert assessment.title == "Test Assessment"
    assert assessment.description == "Test Description"
    assert assessment.scoring_method == ScoringMethod.BOOLEAN
    assert assessment.min_value == 0
    assert assessment.max_value == 1

def test_assessment_default_values():
    assessment = Assessment(
        title="Test Assessment",
        scoring_method=ScoringMethod.BOOLEAN,
        min_value=0,
        max_value=1
    )
    assert assessment.description is None
    assert isinstance(assessment.created_at, datetime)
    assert isinstance(assessment.updated_at, datetime)
    assert assessment.created_at.tzinfo == UTC
    assert assessment.updated_at.tzinfo == UTC

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