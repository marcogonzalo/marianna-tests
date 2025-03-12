import pytest
from sqlmodel import Session
from fastapi import HTTPException
from app.assessments.models import Assessment
from app.users.models import Examinee, Account
from app.responses.schemas import AssessmentResponseCreate, AssessmentResponseUpdate
from app.responses.services import AssessmentResponseService


def test_create_assessment_response(session: Session, sample_assessment: Assessment, sample_examinee: Examinee, sample_account: Account):
    response_data = AssessmentResponseCreate(
        assessment_id=sample_assessment.id,
        examinee_id=sample_examinee.id,
        status="pending",
        created_by=sample_account.id
    )

    response = AssessmentResponseService.create_assessment_response(session, response_data)
    assert response.assessment_id == sample_assessment.id
    assert response.examinee_id == sample_examinee.id
    assert response.status == "pending"
    assert response.created_by == sample_account.id


def test_update_assessment_response(session: Session, sample_assessment: Assessment, sample_examinee: Examinee, sample_account: Account):
    # First, create an assessment response
    response_data = AssessmentResponseCreate(
        assessment_id=sample_assessment.id,
        examinee_id=sample_examinee.id,
        status="pending",
        created_by=sample_account.id
    )

    response = AssessmentResponseService.create_assessment_response(session, response_data)
    
    # Update the response
    updated_response = AssessmentResponseService.update_assessment_response(
        session,
        response.id,
        {"status": "completed", "score": 85.0}
    )

    assert updated_response.status == "completed"
    assert updated_response.score == 85.0


def test_get_assessment_response(session: Session, sample_assessment: Assessment, sample_examinee: Examinee, sample_account: Account):
    response_data = AssessmentResponseCreate(
        assessment_id=sample_assessment.id,
        examinee_id=sample_examinee.id,
        status="pending",
        created_by=sample_account.id
    )

    created_response = AssessmentResponseService.create_assessment_response(session, response_data)
    
    # Get the response
    response = AssessmentResponseService.get_assessment_response(session, created_response.id)
    assert response.id == created_response.id
    assert response.assessment_id == sample_assessment.id
    assert response.examinee_id == sample_examinee.id


def test_list_assessment_responses(session: Session, sample_assessment: Assessment, sample_examinee: Examinee, sample_account: Account):
    # Create multiple assessment responses
    for _ in range(3):
        response_data = AssessmentResponseCreate(
            assessment_id=sample_assessment.id,
            examinee_id=sample_examinee.id,
            status="pending",
            created_by=sample_account.id
        )
        AssessmentResponseService.create_assessment_response(session, response_data)

    # List all responses
    responses = AssessmentResponseService.list_assessment_responses(session, sample_assessment.id)
    assert len(responses) == 3


def test_create_assessment_response_not_found(session: Session, sample_examinee: Examinee, sample_account: Account):
    response_data = AssessmentResponseCreate(
        assessment_id=9999,  # Non-existent assessment ID
        examinee_id=sample_examinee.id,
        status="pending",
        created_by=sample_account.id
    )

    with pytest.raises(HTTPException) as exc_info:
        AssessmentResponseService.create_assessment_response(session, response_data)
    
    assert exc_info.value.status_code == 404
    assert "Assessment not found" in str(exc_info.value.detail)


def test_get_assessment_response_not_found(session: Session):
    with pytest.raises(HTTPException) as exc_info:
        AssessmentResponseService.get_assessment_response(
            session, 9999)  # Non-existent response ID

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Assessment response not found"
