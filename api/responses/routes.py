from fastapi import APIRouter, Depends
from sqlmodel import Session
from .models import ResponseStatus
from .schemas import (
    AssessmentResponseRead,
    BulkQuestionResponseCreate
)
from .services import AssessmentResponseService
from database import get_session

responses_router = APIRouter(prefix="/responses", tags=["responses"])

# Assessment Response endpoints


@responses_router.put("/{response_id}", response_model=AssessmentResponseRead)
async def create_bulk_responses(
    response_id: int,
    bulk_response: BulkQuestionResponseCreate,
    session: Session = Depends(get_session)
):
    assessment_response = AssessmentResponseService.get_assessment_response(
        session, response_id)

    # Create all question responses
    question_responses = []
    total_score = 0
    all_numeric = True

    for response_data in bulk_response.question_responses:
        question_response = AssessmentResponseService.create_question_response(
            session, response_data, response_id)

        if response_data.numeric_value is not None:
            total_score += response_data.numeric_value
        else:
            all_numeric = False

        question_responses.append(question_response)

    # Update assessment response status and score if all responses are numeric
    if all_numeric:
        assessment_response.score = total_score
        assessment_response.status = ResponseStatus.COMPLETED

    session.commit()
    session.refresh(assessment_response)

    return AssessmentResponseRead.from_orm(assessment_response)


@responses_router.get("/{response_id}", response_model=AssessmentResponseRead)
async def get_bulk_responses(
    response_id: int,
    session: Session = Depends(get_session)
):
    assessment_response = AssessmentResponseService.get_assessment_response(
        session, response_id)
    return AssessmentResponseRead.from_orm(assessment_response)
