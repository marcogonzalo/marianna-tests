from datetime import datetime, timezone
from app.responses.services import AssessmentResponseService
from app.responses.models import AssessmentResponse, QuestionResponse
from sqlmodel import Session


def test_assessment_response_creation(session: Session, sample_assessment, sample_examinee, sample_account):
    assessment_response = AssessmentResponse(
        assessment_id=sample_assessment.id,
        examinee_id=sample_examinee.id,
        status="pending",
        created_by=sample_account.id
    )
    session.add(assessment_response)
    session.commit()
    session.refresh(assessment_response)

    assert assessment_response.id is not None
    assert assessment_response.assessment_id == sample_assessment.id
    assert assessment_response.examinee_id == sample_examinee.id
    assert assessment_response.status == "pending"
    assert assessment_response.created_by == sample_account.id
    assert isinstance(assessment_response.created_at, datetime)
    # assert assessment_response.created_at.tzinfo is not None
    # assert assessment_response.created_at.tzinfo == timezone.utc


def test_question_response_creation(session: Session, sample_assessment_response):
    question_response = QuestionResponse(
        assessment_response_id=sample_assessment_response.id,
        question_id=1,  # Assuming a question with ID 1 exists
        numeric_value=5.0,
        text_value="Sample answer"
    )
    session.add(question_response)
    session.commit()
    session.refresh(question_response)

    assert question_response.id is not None
    assert question_response.assessment_response_id == sample_assessment_response.id
    assert question_response.question_id == 1
    assert question_response.numeric_value == 5.0
    assert question_response.text_value == "Sample answer"
    assert isinstance(question_response.created_at, datetime)
    # assert question_response.created_at.tzinfo is not None
    # assert question_response.created_at.tzinfo == timezone.utc


def test_assessment_response_update(session: Session, sample_assessment_response):
    # Update the status of the assessment response
    assessment_response = session.get(
        AssessmentResponse, sample_assessment_response.id)
    assessment_response.status = "completed"
    session.commit()
    session.refresh(assessment_response)

    assert assessment_response.status == "completed"


def test_question_response_update(session: Session, sample_question_response):
    # Update the numeric value of the question response
    question_response = session.get(
        QuestionResponse, sample_question_response.id)
    question_response.numeric_value = 10.0
    session.commit()
    session.refresh(question_response)

    assert question_response.numeric_value == 10.0


def test_assessment_response_deletion(session: Session, sample_assessment_response):
    session.delete(sample_assessment_response)
    session.commit()

    deleted_response = session.get(
        AssessmentResponse, sample_assessment_response.id)
    assert deleted_response is None


def test_question_response_deletion(session: Session, sample_question_response):
    session.delete(sample_question_response)
    session.commit()

    deleted_response = session.get(
        QuestionResponse, sample_question_response.id)
    assert deleted_response is None
