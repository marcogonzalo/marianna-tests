from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
from typing import List
from app.users.enums import UserRole, all_user_roles
from app.auth.services import AuthService, RoleChecker
from database import get_session
from app.responses.schemas import (
    AssessmentResponseCreate, AssessmentResponseCreateParams, AssessmentResponseRead
)
from .models import Assessment, Question, ScoringMethod, Diagnostic
from .schemas import (
    AssessmentCreate, AssessmentRead, AssessmentUpdate,
    QuestionCreate, QuestionRead,
    QuestionUpdate, DiagnosticCreate, DiagnosticRead
)

assessments_router = APIRouter(prefix="/assessments", tags=["assessments"])


# Assessment endpoints

# Protected endpoint - requires authentication
@assessments_router.post("/", response_model=AssessmentRead, dependencies=[Depends(RoleChecker(all_user_roles))])
async def create_assessment(
    assessment: AssessmentCreate,
    session: Session = Depends(get_session)
):
    # Validate custom scoring requirements
    if assessment.scoring_method == ScoringMethod.CUSTOM:
        if assessment.min_value is None or assessment.max_value is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
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
@assessments_router.get("/", response_model=List[AssessmentRead], dependencies=[Depends(RoleChecker(all_user_roles))])
async def list_assessments(session: Session = Depends(get_session)):
    assessments = session.exec(select(Assessment)).all()
    return assessments


# Public endpoint - no authentication required
@assessments_router.get("/{assessment_id}", response_model=AssessmentRead)
async def get_assessment(assessment_id: int, session: Session = Depends(get_session)):
    assessment = session.get(Assessment, assessment_id)
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found")
    return assessment


@assessments_router.patch("/{assessment_id}", response_model=AssessmentRead, dependencies=[Depends(RoleChecker([UserRole.ADMIN, UserRole.ASSESSMENT_DEVELOPER]))])
async def update_assessment(
    assessment_id: int,
    assessment_update: AssessmentUpdate,
    session: Session = Depends(get_session)
):
    db_assessment = session.get(Assessment, assessment_id)
    if not db_assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found")

    assessment_data = assessment_update.model_dump(exclude_unset=True)
    if not assessment_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="No values provided for update")

    for key, value in assessment_data.items():
        setattr(db_assessment, key, value)

    session.add(db_assessment)
    session.commit()
    session.refresh(db_assessment)
    return db_assessment


# Protected endpoint - requires authentication
@assessments_router.delete("/{assessment_id}", dependencies=[Depends(RoleChecker([UserRole.ADMIN, UserRole.ASSESSMENT_DEVELOPER]))])
async def delete_assessment(assessment_id: int, session: Session = Depends(get_session)):
    assessment = session.get(Assessment, assessment_id)
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found")

    session.delete(assessment)
    session.commit()
    return {"message": "Assessment deleted"}

# Question endpoints - all protected


@assessments_router.post("/{assessment_id}/questions", response_model=QuestionRead, dependencies=[Depends(RoleChecker([UserRole.ADMIN, UserRole.ASSESSMENT_DEVELOPER]))])
async def create_question(
    assessment_id: int,
    question: QuestionCreate,
    session: Session = Depends(get_session)
):
    db_assessment = session.get(Assessment, assessment_id)
    if not db_assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found")

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


@assessments_router.get("/{assessment_id}/questions", response_model=List[QuestionRead], dependencies=[Depends(RoleChecker(all_user_roles))])
async def list_questions(assessment_id: int, session: Session = Depends(get_session)):
    questions = session.exec(
        select(Question).where(Question.assessment_id == assessment_id)
    ).all()
    return questions


@assessments_router.put("/{assessment_id}/questions/bulk", response_model=List[QuestionRead], dependencies=[Depends(RoleChecker([UserRole.ADMIN, UserRole.ASSESSMENT_DEVELOPER]))])
async def bulk_update_questions(
    assessment_id: int,
    questions: List[QuestionUpdate],
    session: Session = Depends(get_session)
):
    # Get existing questions
    existing_questions = session.exec(
        select(Question).where(Question.assessment_id == assessment_id)
    ).all()

    # Create a map of existing questions by ID
    existing_questions_map = {q.id: q for q in existing_questions}

    # Track which questions we've processed
    processed_ids = set()

    updated_questions = []

    for question_data in questions:
        if question_data.id and question_data.id in existing_questions_map:
            # Update existing question
            question = existing_questions_map[question_data.id]
            question.update_attributes(question_data)
            processed_ids.add(question_data.id)
        else:
            # Create new question
            new_question = Question(
                text=question_data.text,
                order=question_data.order,
                assessment_id=assessment_id
            )
            session.add(new_question)
            session.flush()  # Get the ID for the new question
            question = new_question

        question.alter_choice_list(question_data.choices, session)
        updated_questions.append(question)

    # Delete questions that weren't in the update list
    for question_id, question in existing_questions_map.items():
        if question_id not in processed_ids:
            session.delete(question)

    session.commit()

    # Refresh all questions to get their updated state
    for question in updated_questions:
        session.refresh(question)

    return updated_questions


@assessments_router.get("/{assessment_id}/questions/{question_id}", response_model=QuestionRead, dependencies=[Depends(RoleChecker(all_user_roles))])
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
    return question


@assessments_router.put("/{assessment_id}/questions/{question_id}", response_model=QuestionRead, dependencies=[Depends(RoleChecker([UserRole.ADMIN, UserRole.ASSESSMENT_DEVELOPER]))])
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


@assessments_router.delete("/{assessment_id}/questions/{question_id}", dependencies=[Depends(RoleChecker([UserRole.ADMIN, UserRole.ASSESSMENT_DEVELOPER]))])
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")

    session.delete(question)
    session.commit()
    return {"message": "Question deleted"}


# Diagnostic endpoints - all protected
@assessments_router.post("/{assessment_id}/diagnostics", response_model=DiagnosticRead, dependencies=[Depends(RoleChecker([UserRole.ADMIN, UserRole.ASSESSMENT_DEVELOPER]))])
async def create_diagnostic(
    assessment_id: int,
    diagnostic: DiagnosticCreate,
    session: Session = Depends(get_session)
):
    db_assessment = session.get(Assessment, assessment_id)
    if not db_assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found")

    db_diagnostic = Diagnostic(
        **diagnostic.model_dump(),
        assessment_id=assessment_id
    )
    session.add(db_diagnostic)
    session.commit()
    session.refresh(db_diagnostic)
    return db_diagnostic


@assessments_router.get("/{assessment_id}/diagnostics", response_model=List[DiagnosticRead], dependencies=[Depends(RoleChecker(all_user_roles))])
async def list_diagnostics(assessment_id: int, session: Session = Depends(get_session)):
    diagnostics = session.exec(
        select(Diagnostic).where(Diagnostic.assessment_id == assessment_id)
    ).all()
    return diagnostics

# Assessment Response endpoints


@assessments_router.post("/{assessment_id}/responses", response_model=AssessmentResponseRead, dependencies=[Depends(RoleChecker([UserRole.ADMIN, UserRole.ASSESSMENT_DEVELOPER]))])
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found")

    examinee = session.get(Examinee, assessment_response_params.examinee_id)
    if not examinee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Examinee not found")

    # Create new assessment response
    assessment_response = AssessmentResponseService.create_assessment_response(
        session, AssessmentResponseCreate(**assessment_response_params.model_dump(), assessment_id=assessment_id, created_by=current_user.account.id))

    session.add(assessment_response)
    session.commit()
    session.refresh(assessment_response)

    AssessmentResponseService.send_link_by_email(
        response=AssessmentResponseRead.model_validate(assessment_response),
        examinee=ExamineeRead.model_validate(
            assessment_response.examinee.model_dump()),
        current_user=UserRead.model_validate(current_user)
    )

    return AssessmentResponseRead.model_validate(assessment_response)
