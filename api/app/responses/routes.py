import os
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlmodel import Session
from app.responses.models import ResponseStatus
from app.auth.services import AuthService
from app.auth.security import oauth2_scheme_optional
from app.assessments.schemas import AssessmentBase, AssessmentRead
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
    query_params: dict = Depends(get_query_params), current_user=Depends(AuthService.get_current_active_user)
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
            response_dict['assessment'] = AssessmentBase.model_validate(
                assessment_dict)
            validated_responses.append(
                AssessmentResponseReadWithAssessment.model_validate(response_dict))

    return validated_responses


@responses_router.patch("/{response_id}/change-status", response_model=AssessmentResponseRead)
async def change_status(
    response_id: str,
    status_update: AssessmentResponseUpdate,
    session: Session = Depends(get_session),
    current_user=Depends(AuthService.get_current_active_user)
):
    # Pass the ID directly and let the service handle getting the database model
    assessment_response = AssessmentResponseService.update_assessment_response_status_and_score(
        session, response_id, status_update.status)

    return AssessmentResponseRead.model_validate(assessment_response)


@responses_router.put("/{response_id}", response_model=AssessmentResponseRead)
async def create_bulk_responses(
    response_id: str,
    bulk_response: BulkQuestionResponseCreate,
    session: Session = Depends(get_session)
):
    assessment_response = AssessmentResponseService.create_question_responses_bulk(
        session, response_id, bulk_response)
    if assessment_response.status == ResponseStatus.COMPLETED:
        from app.users.schemas import ExamineeRead, UserRead
        examinee = assessment_response.examinee
        user = assessment_response.creator.user
        await AssessmentResponseService.notify_examinee_completed_assessment(
            response=AssessmentResponseRead.model_validate(assessment_response),
            examinee=ExamineeRead.model_validate(examinee.__dict__),
            user=UserRead.model_validate(user)
        )
    return AssessmentResponseRead.model_validate(assessment_response)


@ responses_router.get("/{response_id}", response_model=AssessmentResponseReadWithQuestions)
async def get_bulk_responses(
    response_id: str,
    session: Session=Depends(get_session),
    token: str | None=Depends(oauth2_scheme_optional)
):
    response_dict=AssessmentResponseService.get_assessment_response(
        session, response_id)

    if response_dict['status'] != ResponseStatus.PENDING:
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required for non-pending responses",
                headers={"WWW-Authenticate": "Bearer"},
            )

    # Handle nested assessment validation
    if 'assessment' in response_dict:
        assessment_dict=response_dict['assessment']
        response_dict['assessment']=AssessmentRead.model_validate(
            assessment_dict)
    print("response_dict", response_dict)
    if 'question_responses' in response_dict:
        question_responses_dict=response_dict['question_responses']
        validated_question_responses=[]
        print("question_responses_dict", question_responses_dict)
        for question_response in question_responses_dict:
            validated_question_responses.append(QuestionResponseRead.model_validate(
                question_response))
            print("validated_question_responses", validated_question_responses)
        response_dict['question_responses']=validated_question_responses

    # Validate the complete response
    return AssessmentResponseReadWithQuestions.model_validate(response_dict)
