from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from assessments.models import Question
from database import get_session
from .models import AssessmentResponse, QuestionResponse, ResponseStatus
from .schemas import (
    QuestionResponseRead,
    AssessmentResponseRead,
    BulkQuestionResponseCreate
)

responses_router = APIRouter(prefix="/responses", tags=["responses"])

# Assessment Response endpoints


@responses_router.put("/{response_id}", response_model=AssessmentResponseRead)
async def create_bulk_responses(
    response_id: int,
    bulk_response: BulkQuestionResponseCreate,
    session: Session = Depends(get_session)
):
    assessment_response = session.get(AssessmentResponse, response_id)
    if not assessment_response:
        raise HTTPException(
            status_code=404, detail="Assessment response not found")

    # Create all question responses
    question_responses = []
    total_score = 0
    all_numeric = True

    for response_data in bulk_response.question_responses:
        question = session.get(Question, response_data.question_id)
        if not question:
            raise HTTPException(
                status_code=404,
                detail=f"Question {response_data.question_id} not found"
            )

        question_response = QuestionResponse(
            assessment_response_id=response_id,
            question_id=response_data.question_id,
            numeric_value=response_data.numeric_value,
            text_value=response_data.text_value
        )

        if response_data.numeric_value is not None:
            total_score += response_data.numeric_value
        else:
            all_numeric = False

        session.add(question_response)
        question_responses.append(question_response)

    # Update assessment response status and score if all responses are numeric
    if all_numeric:
        assessment_response.score = total_score
        assessment_response.status = ResponseStatus.COMPLETED

    session.commit()
    session.refresh(assessment_response)

    # Convert QuestionResponse models to QuestionResponseRead before returning
    question_responses_read = [
        QuestionResponseRead(
            id=qr.id,
            question_id=qr.question_id,
            assessment_response_id=qr.assessment_response_id,
            numeric_value=qr.numeric_value,
            text_value=qr.text_value,
            created_at=qr.created_at
        ) for qr in assessment_response.question_responses
    ]

    return AssessmentResponseRead(
        id=assessment_response.id,
        assessment_id=assessment_response.assessment_id,
        status=assessment_response.status,
        score=assessment_response.score,
        question_responses=question_responses_read,
        created_at=assessment_response.created_at,
        updated_at=assessment_response.updated_at
    )


@responses_router.get("/{response_id}", response_model=AssessmentResponseRead)
async def get_bulk_responses(
    response_id: int,
    session: Session = Depends(get_session)
):
    # Get the assessment response with relationships
    assessment_response = session.get(AssessmentResponse, response_id)
    if not assessment_response:
        raise HTTPException(
            status_code=404, detail="Assessment response not found")

    # Get all question responses for this assessment response
    question_responses = session.exec(
        select(QuestionResponse)
        .where(QuestionResponse.assessment_response_id == response_id)
    ).all()

    # Return complete assessment response data
    return AssessmentResponseRead(
        id=assessment_response.id,
        assessment_id=assessment_response.assessment_id,
        status=assessment_response.status,
        score=assessment_response.score,
        question_responses=question_responses,
        created_at=assessment_response.created_at,
        updated_at=assessment_response.updated_at
    )
