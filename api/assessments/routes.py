from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from typing import List
from .models import Assessment, Question, AnswerOption
from .schemas import AssessmentCreate, AssessmentRead, QuestionCreate, QuestionRead

router = APIRouter(prefix="/assessments", tags=["assessments"])

from database import get_session

@router.post("/", response_model=AssessmentRead)
async def create_assessment(assessment: AssessmentCreate, session: Session = Depends(get_session)):
    db_assessment = Assessment(**assessment.dict(exclude={"questions"}))
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
