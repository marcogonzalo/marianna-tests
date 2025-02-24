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


@responses_router.put("/{response_id}", response_model=AssessmentResponseRead)
async def create_bulk_responses(
    response_id: str,
    bulk_response: BulkQuestionResponseCreate,
    session: Session = Depends(get_session)
):
    assessment_response = AssessmentResponseService.get_assessment_response(
        session, response_id)

    # Create all question responses
    question_responses = []
    total_score = 0
    # all_numeric = True

    for response_data in bulk_response.question_responses:
        question_response = AssessmentResponseService.create_question_response(
            session, response_data, response_id)

        if response_data.numeric_value is not None:
            total_score += response_data.numeric_value
        # else:
        #     all_numeric = False

        question_responses.append(question_response)

    # Update assessment response status and score if all responses are numeric
    # if all_numeric:
    assessment_response.score = total_score
    assessment_response.status = ResponseStatus.COMPLETED

    session.commit()
    session.refresh(assessment_response)

    return AssessmentResponseRead.model_validate(assessment_response)


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

    assessment_response.status = status_update.status
    session.add(assessment_response)
    session.commit()
    session.refresh(assessment_response)
    return AssessmentResponseRead.model_validate(assessment_response)


@responses_router.get("/{response_id}", response_model=AssessmentResponseReadWithQuestions)
async def get_bulk_responses(
    response_id: str,
    session: Session = Depends(get_session)
):
    assessment_response = AssessmentResponseService.get_assessment_response(
        session, response_id)

    # Convert the main response to a dictionary
    response_dict = assessment_response.model_dump()

    # Handle nested assessment validation
    if assessment_response.assessment:
        assessment_dict = assessment_response.assessment.model_dump()
        response_dict['assessment'] = AssessmentRead.model_validate(
            assessment_dict)

    if assessment_response.assessment:
        question_responses_dict = assessment_response.question_responses
        validated_question_responses = []
        for question_response in question_responses_dict:
            validated_question_responses.append(QuestionResponseRead.model_validate(
                question_response.model_dump()))
        response_dict['question_responses'] = validated_question_responses

    # Validate the complete response
    return AssessmentResponseReadWithQuestions.model_validate(response_dict)
