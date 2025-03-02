from fastapi import APIRouter, Depends, Request
from sqlmodel import Session

from assessments.schemas import AssessmentRead
from .models import ResponseStatus
from .schemas import (
    AssessmentResponseRead,
    AssessmentResponseReadWithAssessment,
    AssessmentResponseReadWithQuestions,
    AssessmentResponseUpdate,
    BulkQuestionResponseCreate,
    QuestionResponseRead
)
from .services import AssessmentResponseService
from database import get_session

responses_router = APIRouter(prefix="/responses", tags=["responses"])

# Assessment Response endpoints


async def get_query_params(request: Request):
    return request.query_params


@responses_router.get("/", response_model=list[AssessmentResponseReadWithAssessment])
async def get_assessment_responses(
    session: Session = Depends(get_session),
    query_params: dict = Depends(get_query_params)
):
    if 'examinee' in query_params:
        assessment_responses = AssessmentResponseService.get_assessment_responses_by_examinee(
            session, query_params["examinee_id"])
    else:
        assessment_responses = AssessmentResponseService.get_all_assessment_responses(
            session)

    # Convert SQLModel instances to dictionaries first
    validated_responses = []
    for response in assessment_responses:
        # Convert the assessment to a dictionary first
        if response.assessment:
            assessment_dict = response.assessment.model_dump()
            response_dict = response.model_dump()
            response_dict['assessment'] = AssessmentRead.model_validate(
                assessment_dict)
            validated_responses.append(
                AssessmentResponseReadWithAssessment.model_validate(response_dict))

    return validated_responses


@responses_router.patch("/{response_id}/change-status", response_model=AssessmentResponseRead)
async def change_status(
    response_id: str,
    status_update: AssessmentResponseUpdate,
    session: Session = Depends(get_session)
):
    assessment_response = AssessmentResponseService.get_assessment_response(
        session, response_id)

    if assessment_response is None:
        return {"error": "Assessment response not found"}, 404

    AssessmentResponseService.update_assessment_response_status_and_score(
        session, assessment_response, status_update.status)

    return AssessmentResponseRead.model_validate(assessment_response)


@responses_router.put("/{response_id}", response_model=AssessmentResponseRead)
async def create_bulk_responses(
    response_id: str,
    bulk_response: BulkQuestionResponseCreate,
    session: Session = Depends(get_session)
):
    assessment_response = AssessmentResponseService.get_assessment_response(
        session, response_id)

    # Create all question responses and calculate the total score

    # Update assessment response status and score
    assessment_response = AssessmentResponseService.create_question_responses_bulk(
        session, assessment_response, bulk_response)

    return AssessmentResponseRead.model_validate(assessment_response)


@responses_router.get("/{response_id}", response_model=AssessmentResponseReadWithQuestions)
async def get_bulk_responses(
    response_id: str,
    session: Session = Depends(get_session)
):
    response_dict = AssessmentResponseService.get_assessment_response(
        session, response_id)

    # Handle nested assessment validation
    if 'assessment' in response_dict:
        assessment_dict = response_dict['assessment']
        response_dict['assessment'] = AssessmentRead.model_validate(
            assessment_dict)

    if 'question_responses' in response_dict:
        question_responses_dict = response_dict['question_responses']
        validated_question_responses = []
        for question_response in question_responses_dict:
            validated_question_responses.append(QuestionResponseRead.model_validate(
                question_response))
        response_dict['question_responses'] = validated_question_responses

    # Validate the complete response
    return AssessmentResponseReadWithQuestions.model_validate(response_dict)
