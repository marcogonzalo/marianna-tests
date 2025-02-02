from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from typing import List
from .models import Assessment, Question, Choice
from .schemas import (
    AssessmentCreate, AssessmentRead,
    QuestionCreate, QuestionRead,
    # ChoiceCreate, ChoiceRead,
    QuestionUpdate  # Add this import
)

router = APIRouter(prefix="/assessments", tags=["assessments"])

from database import get_session

# Assessment endpoints
@router.post("/", response_model=AssessmentRead)
async def create_assessment(assessment: AssessmentCreate, session: Session = Depends(get_session)):
    db_assessment = Assessment(**assessment.dict(exclude={"questions"}))
    if not (assessment.min_value or assessment.max_value):
        db_assessment.set_default_values()
    session.add(db_assessment)
    session.commit()
    session.refresh(db_assessment)
    return db_assessment

@router.get("/", response_model=List[AssessmentRead])
async def list_assessments(session: Session = Depends(get_session)):
    assessments = session.exec(select(Assessment)).all()
    return assessments

@router.get("/{assessment_id}", response_model=AssessmentRead)
async def get_assessment(assessment_id: int, session: Session = Depends(get_session)):
    assessment = session.get(Assessment, assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return assessment

@router.put("/{assessment_id}", response_model=AssessmentRead)
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

@router.delete("/{assessment_id}")
async def delete_assessment(assessment_id: int, session: Session = Depends(get_session)):
    assessment = session.get(Assessment, assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    session.delete(assessment)
    session.commit()
    return {"message": "Assessment deleted"}

# Question endpoints
@router.post("/{assessment_id}/questions", response_model=QuestionRead)
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

    # Create choices
    for choice_data in question.choices:
        db_choice = Choice(
            text=choice_data.text,
            value=choice_data.value,
            order=choice_data.order,
            question_id=db_question.id
        )
        session.add(db_choice)

    session.commit()
    session.refresh(db_question)
    return db_question

@router.get("/{assessment_id}/questions", response_model=List[QuestionRead])
async def list_questions(assessment_id: int, session: Session = Depends(get_session)):
    questions = session.exec(
        select(Question).where(Question.assessment_id == assessment_id)
    ).all()
    return questions

@router.get("/{assessment_id}/questions/{question_id}", response_model=QuestionRead)
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

@router.put("/{assessment_id}/questions/{question_id}", response_model=QuestionRead)
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
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Update question data
    question.update_attributes(question_update)

    # Update question choice list
    question.alter_choice_list(question_update.choices, session)

    session.add(question)
    session.commit()
    session.refresh(question)
    return question

@router.delete("/{assessment_id}/questions/{question_id}")
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
