from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from typing import List
from app.auth.services import AuthService
from database import get_session
from app.responses.schemas import (
    AssessmentResponseCreate, AssessmentResponseCreateParams, AssessmentResponseRead
)
from .models import Assessment, Question, ScoringMethod, Diagnostic
from .schemas import (
    AssessmentCreate, AssessmentRead,
    QuestionCreate, QuestionRead,
    QuestionUpdate, DiagnosticCreate, DiagnosticRead
)

assessments_router = APIRouter(prefix="/assessments", tags=["assessments"])


# Assessment endpoints

# Protected endpoint - requires authentication
@assessments_router.post("/", response_model=AssessmentRead)
async def create_assessment(
    assessment: AssessmentCreate,
    session: Session = Depends(get_session), current_user=Depends(AuthService.get_current_active_user)
):
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


# Protected endpoint - requires authentication
@assessments_router.get("/", response_model=List[AssessmentRead])
async def list_assessments(session: Session = Depends(get_session), current_user=Depends(AuthService.get_current_active_user)):
    assessments = session.exec(select(Assessment)).all()
    return assessments


# Public endpoint - no authentication required
@assessments_router.get("/{assessment_id}", response_model=AssessmentRead)
async def get_assessment(assessment_id: int, session: Session = Depends(get_session)):
    assessment = session.get(Assessment, assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return assessment


# Protected endpoint - requires authentication
@assessments_router.put("/{assessment_id}", response_model=AssessmentRead)
async def update_assessment(
    assessment_id: int,
    assessment_update: AssessmentCreate,
    session: Session = Depends(get_session), current_user=Depends(AuthService.get_current_active_user)
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


# Protected endpoint - requires authentication
@assessments_router.delete("/{assessment_id}")
async def delete_assessment(assessment_id: int, session: Session = Depends(get_session), current_user=Depends(AuthService.get_current_active_user)):
    assessment = session.get(Assessment, assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    session.delete(assessment)
    session.commit()
    return {"message": "Assessment deleted"}

# Question endpoints - all protected


@assessments_router.post("/{assessment_id}/questions", response_model=QuestionRead)
async def create_question(
    assessment_id: int,
    question: QuestionCreate,
    session: Session = Depends(get_session), current_user=Depends(AuthService.get_current_active_user)
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
async def list_questions(assessment_id: int, session: Session = Depends(get_session), current_user=Depends(AuthService.get_current_active_user)):
    questions = session.exec(
        select(Question).where(Question.assessment_id == assessment_id)
    ).all()
    return questions


@assessments_router.get("/{assessment_id}/questions/{question_id}", response_model=QuestionRead)
async def get_question(
    assessment_id: int,
    question_id: int,
    session: Session = Depends(get_session), current_user=Depends(AuthService.get_current_active_user)
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
    session: Session = Depends(get_session), current_user=Depends(AuthService.get_current_active_user)
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
    session: Session = Depends(get_session), current_user=Depends(AuthService.get_current_active_user)
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


# Diagnostic endpoints - all protected
@assessments_router.post("/{assessment_id}/diagnostics", response_model=DiagnosticRead)
async def create_diagnostic(
    assessment_id: int,
    diagnostic: DiagnosticCreate,
    session: Session = Depends(get_session), current_user=Depends(AuthService.get_current_active_user)
):
    db_assessment = session.get(Assessment, assessment_id)
    if not db_assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    db_diagnostic = Diagnostic(
        **diagnostic.model_dump(),
        assessment_id=assessment_id
    )
    session.add(db_diagnostic)
    session.commit()
    session.refresh(db_diagnostic)
    return db_diagnostic


@assessments_router.get("/{assessment_id}/diagnostics", response_model=List[DiagnosticRead])
async def list_diagnostics(assessment_id: int, session: Session = Depends(get_session), current_user=Depends(AuthService.get_current_active_user)):
    diagnostics = session.exec(
        select(Diagnostic).where(Diagnostic.assessment_id == assessment_id)
    ).all()
    return diagnostics

# Assessment Response endpoints


@assessments_router.post("/{assessment_id}/responses", response_model=AssessmentResponseRead)
async def create_assessment_response(
    assessment_id: int,
    assessment_response_params: AssessmentResponseCreateParams,
    session: Session = Depends(get_session), current_user=Depends(AuthService.get_current_active_user)
):
    from app.users.models import Examinee
    from app.users.schemas import ExamineeRead, UserRead
    from app.responses.services import AssessmentResponseService

    # Verify assessment exists
    assessment = session.get(Assessment, assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    examinee = session.get(Examinee, assessment_response_params.examinee_id)
    if not examinee:
        raise HTTPException(status_code=404, detail="Examinee not found")

    # Create new assessment response
    assessment_response = AssessmentResponseService.create_assessment_response(
        session, AssessmentResponseCreate(**assessment_response_params.model_dump(), assessment_id=assessment_id, created_by=current_user.account.id))

    session.add(assessment_response)
    session.commit()
    session.refresh(assessment_response)

    await AssessmentResponseService.send_link_by_email(
        response=AssessmentResponseRead.model_validate(assessment_response),
        examinee=ExamineeRead.model_validate(assessment_response.examinee.model_dump()),
        current_user=UserRead.model_validate(current_user)
    )

    return AssessmentResponseRead.model_validate(assessment_response)
