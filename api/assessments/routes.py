from fastapi import APIRouter, HTTPException, Depends
from pydantic import UUID4
from sqlmodel import Session, select
from typing import List
from database import get_session
from responses.schemas import AssessmentResponseRead, AssessmentResponseRead
from .models import Assessment, Question, ScoringMethod
from .schemas import (
    AssessmentCreate, AssessmentRead, AssessmentResponseCreateParams,
    QuestionCreate, QuestionRead,
    QuestionUpdate,
)

assessments_router = APIRouter(prefix="/assessments", tags=["assessments"])


# Assessment endpoints

@assessments_router.post("/", response_model=AssessmentRead)
async def create_assessment(assessment: AssessmentCreate, session: Session = Depends(get_session)):
    # Validate custom scoring requirements
    if assessment.scoring_method == ScoringMethod.CUSTOM:
        if assessment.min_value is None or assessment.max_value is None:
            raise HTTPException(
                status_code=422,
                detail="Custom scoring method requires explicit min_value and max_value"
            )

    db_assessment = Assessment(**assessment.dict(exclude={"questions"}))

    if not assessment.min_value and not assessment.max_value:
        db_assessment.set_default_values()

    session.add(db_assessment)
    session.commit()
    session.refresh(db_assessment)
    return db_assessment


@assessments_router.get("/", response_model=List[AssessmentRead])
async def list_assessments(session: Session = Depends(get_session)):
    assessments = session.exec(select(Assessment)).all()
    return assessments


@assessments_router.get("/{assessment_id}", response_model=AssessmentRead)
async def get_assessment(assessment_id: int, session: Session = Depends(get_session)):
    assessment = session.get(Assessment, assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return assessment


@assessments_router.put("/{assessment_id}", response_model=AssessmentRead)
async def update_assessment(
    assessment_id: int,
    assessment_update: AssessmentCreate,
    session: Session = Depends(get_session)
):
    db_assessment = session.get(Assessment, assessment_id)
    if not db_assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    assessment_data = assessment_update.dict(exclude_unset=True)
    for key, value in assessment_data.items():
        setattr(db_assessment, key, value)

    session.add(db_assessment)
    session.commit()
    session.refresh(db_assessment)
    return db_assessment


@assessments_router.delete("/{assessment_id}")
async def delete_assessment(assessment_id: int, session: Session = Depends(get_session)):
    assessment = session.get(Assessment, assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    session.delete(assessment)
    session.commit()
    return {"message": "Assessment deleted"}

# Question endpoints


@assessments_router.post("/{assessment_id}/questions", response_model=QuestionRead)
async def create_question(
    assessment_id: int,
    question: QuestionCreate,
    session: Session = Depends(get_session)
):
    db_assessment = session.get(Assessment, assessment_id)
    if not db_assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    db_question = Question(
        text=question.text,
        order=question.order,
        assessment_id=assessment_id
    )
    session.add(db_question)
    session.commit()
    session.refresh(db_question)

    db_question.alter_choice_list(question.choices, session)

    session.commit()
    session.refresh(db_question)
    return db_question


@assessments_router.get("/{assessment_id}/questions", response_model=List[QuestionRead])
async def list_questions(assessment_id: int, session: Session = Depends(get_session)):
    questions = session.exec(
        select(Question).where(Question.assessment_id == assessment_id)
    ).all()
    return questions


@assessments_router.get("/{assessment_id}/questions/{question_id}", response_model=QuestionRead)
async def get_question(
    assessment_id: int,
    question_id: int,
    session: Session = Depends(get_session)
):
    question = session.exec(
        select(Question)
        .where(Question.assessment_id == assessment_id)
        .where(Question.id == question_id)
    ).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


@assessments_router.put("/{assessment_id}/questions/{question_id}", response_model=QuestionRead)
async def update_question(
    assessment_id: int,
    question_id: int,
    question_update: QuestionUpdate,  # Changed from QuestionCreate to QuestionUpdate
    session: Session = Depends(get_session)
):
    # Get existing question
    question = session.exec(
        select(Question)
        .where(Question.assessment_id == assessment_id)
        .where(Question.id == question_id)
    ).first()

    # Update question data
    question.update_attributes(question_update)

    # Update question choice list
    question.alter_choice_list(question_update.choices, session)

    session.add(question)
    session.commit()
    session.refresh(question)
    return question


@assessments_router.delete("/{assessment_id}/questions/{question_id}")
async def delete_question(
    assessment_id: int,
    question_id: int,
    session: Session = Depends(get_session)
):
    question = session.exec(
        select(Question)
        .where(Question.assessment_id == assessment_id)
        .where(Question.id == question_id)
    ).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    session.delete(question)
    session.commit()
    return {"message": "Question deleted"}

# Assessment Response endpoints


@assessments_router.get("/{assessment_id}/responses", response_model=List["AssessmentResponseRead"])
async def list_assessment_responses(
    assessment_id: int,
    session: Session = Depends(get_session)
):
    responses = session.exec(
        select("AssessmentResponse")
        .where("AssessmentResponse".assessment_id == assessment_id)
    ).all()
    return responses


@assessments_router.post("/{assessment_id}/responses", response_model=AssessmentResponseRead)
async def create_assessment_response(
    assessment_id: int,
    assessment_response_params: AssessmentResponseCreateParams,
    session: Session = Depends(get_session)
):
    from users.models import Examinee
    from responses.models import AssessmentResponse, ResponseStatus

    # Verify assessment exists
    assessment = session.get(Assessment, assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    examinee = session.get(Examinee, assessment_response_params.examinee_id)
    if not examinee:
        raise HTTPException(status_code=404, detail="Examinee not found")
    # Create new assessment response
    assessment_response = AssessmentResponse(
        assessment_id=assessment.id,
        examinee_id=examinee.id,
        status=ResponseStatus.PENDING,
        score=None  # Initialize score as None
    )

    session.add(assessment_response)
    session.commit()
    session.refresh(assessment_response)

    return AssessmentResponseRead(
        id=assessment_response.id,
        assessment_id=assessment_response.assessment_id,
        examinee_id=assessment_response.examinee_id,
        status=assessment_response.status,
        score=assessment_response.score,
        question_responses=[],  # Initialize with empty list
        created_at=assessment_response.created_at,
        updated_at=assessment_response.updated_at
    )
