import pytest
from assessments.schemas import AssessmentRead
from assessments.models import Assessment
from responses.schemas import (
    AssessmentResponseCreate,
    AssessmentResponseReadWithQuestions,
    AssessmentResponseUpdate,
    BulkQuestionResponseCreate,
    QuestionResponseCreate,
    QuestionResponseRead
)
from responses.models import ResponseStatus
from pydantic import ValidationError
from uuid import uuid4


def test_assessment_response_create_validation():
    # Valid assessment response creation
    response = AssessmentResponseCreate(
        assessment_id=1,
        examinee_id=uuid4(),
        status=ResponseStatus.PENDING
    )
    assert response.assessment_id == 1
    assert response.examinee_id is not None
    assert response.status == ResponseStatus.PENDING

    # Invalid assessment response (missing examinee_id)
    with pytest.raises(ValidationError):
        AssessmentResponseCreate(
            assessment_id=1,
            examinee_id=None,  # Invalid UUID
            status=ResponseStatus.PENDING
        )


def test_assessment_response_update_validation():
    # Valid update
    update = AssessmentResponseUpdate(
        status=ResponseStatus.COMPLETED,
        score=85.0
    )
    assert update.status == ResponseStatus.COMPLETED
    assert update.score == 85.0

    # Invalid update (missing status)
    with pytest.raises(ValidationError):
        AssessmentResponseUpdate(
            status=None,  # Invalid status
            score=85.0
        )


def test_assessment_response_read_with__validation(sample_assessment: Assessment):
    # Convert SQLModel to dict first, then to AssessmentRead
    assessment_dict = sample_assessment.model_dump()
    assessment_read = AssessmentRead(**assessment_dict)

    # Valid read
    response = AssessmentResponseReadWithQuestions(
        id="some_id",
        status=ResponseStatus.PENDING,
        score=None,
        assessment_id=sample_assessment.id,
        assessment=assessment_read,
        question_responses=[],
        examinee_id=uuid4()
    )
    assert response.id == "some_id"
    assert response.status == ResponseStatus.PENDING
    assert response.assessment_id == sample_assessment.id
    assert response.assessment.id == sample_assessment.id
    assert len(response.question_responses) == 0


def test_bulk_question_response_create_validation():
    # Valid bulk question response
    bulk_response = BulkQuestionResponseCreate(
        question_responses=[
            QuestionResponseCreate(
                numeric_value=5.0, text_value=None, question_id=1),
            QuestionResponseCreate(text_value="Sample answer", question_id=2)
        ]
    )
    assert len(bulk_response.question_responses) == 2

    # Invalid bulk question response (no responses)
    with pytest.raises(ValidationError):
        BulkQuestionResponseCreate(
            question_responses=[]
        )


def test_question_response_create_validation():
    # Valid question response
    question_response = QuestionResponseCreate(
        numeric_value=5.0,
        text_value=None,
        question_id=1
    )
    assert question_response.numeric_value == 5.0
    assert question_response.question_id == 1

    # Invalid question response (both values None)
    with pytest.raises(ValidationError):
        QuestionResponseCreate(
            numeric_value=None,
            text_value=None,
            question_id=1
        )


def test_question_response_read_validation():
    # Valid question response read
    assessment_response_id = str(uuid4())
    question_response_read = QuestionResponseRead(
        id=1,
        numeric_value=5.0,
        text_value=None,
        question_id=1,
        assessment_response_id=assessment_response_id
    )
    assert question_response_read.id == 1
    assert question_response_read.numeric_value == 5.0
    assert question_response_read.assessment_response_id == assessment_response_id
