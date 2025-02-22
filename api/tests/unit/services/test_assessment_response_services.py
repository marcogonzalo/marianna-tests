import pytest
from sqlmodel import Session
from fastapi import HTTPException
from assessments.models import Assessment
from users.models import Examinee
from responses.schemas import AssessmentResponseCreate, AssessmentResponseUpdate
from responses.services import AssessmentResponseService


def test_create_assessment_response(session: Session, sample_assessment: Assessment, sample_examinee: Examinee):
    response_data = AssessmentResponseCreate(
        assessment_id=sample_assessment.id,
        examinee_id=sample_examinee.id,
        status="pending"
    )

    assessment_response = AssessmentResponseService.create_assessment_response(
        session, response_data)

    assert assessment_response.id is not None
    assert assessment_response.assessment_id == sample_assessment.id
    assert assessment_response.examinee_id == sample_examinee.id
    assert assessment_response.status == "pending"


def test_update_assessment_response(session: Session, sample_assessment: Assessment, sample_examinee: Examinee):
    # First, create an assessment response
    response_data = AssessmentResponseCreate(
        assessment_id=sample_assessment.id,
        examinee_id=sample_examinee.id,
        status="pending"
    )
    assessment_response = AssessmentResponseService.create_assessment_response(
        session, response_data)

    # Now, update the assessment response
    update_data = AssessmentResponseUpdate(status="completed", score=85.0)
    updated_response = AssessmentResponseService.update_assessment_response(
        session, assessment_response.id, update_data)

    assert updated_response.status == "completed"
    assert updated_response.score == 85.0


def test_get_assessment_response(session: Session, sample_assessment: Assessment, sample_examinee: Examinee):
    response_data = AssessmentResponseCreate(
        assessment_id=sample_assessment.id,
        examinee_id=sample_examinee.id,
        status="pending"
    )
    assessment_response = AssessmentResponseService.create_assessment_response(
        session, response_data)

    retrieved_response = AssessmentResponseService.get_assessment_response(
        session, assessment_response.id)

    assert retrieved_response.id == assessment_response.id
    assert retrieved_response.assessment_id == sample_assessment.id
    assert retrieved_response.examinee_id == sample_examinee.id


def test_list_assessment_responses(session: Session, sample_assessment: Assessment, sample_examinee: Examinee):
    # Create multiple assessment responses
    for _ in range(3):
        response_data = AssessmentResponseCreate(
            assessment_id=sample_assessment.id,
            examinee_id=sample_examinee.id,
            status="pending"
        )
        AssessmentResponseService.create_assessment_response(
            session, response_data)

    responses = AssessmentResponseService.list_assessment_responses(
        session, sample_assessment.id)

    # Expecting 3 responses for the created assessment
    assert len(responses) == 3


def test_create_assessment_response_not_found(session: Session, sample_examinee: Examinee):
    response_data = AssessmentResponseCreate(
        assessment_id=9999,  # Non-existent assessment ID
        examinee_id=sample_examinee.id,
        status="pending"
    )

    with pytest.raises(HTTPException) as exc_info:
        AssessmentResponseService.create_assessment_response(
            session, response_data)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Assessment not found"


def test_get_assessment_response_not_found(session: Session):
    with pytest.raises(HTTPException) as exc_info:
        AssessmentResponseService.get_assessment_response(
            session, 9999)  # Non-existent response ID

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Assessment response not found"
