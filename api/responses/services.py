from typing import List
from pydantic import UUID4
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException
from .models import AssessmentResponse, QuestionResponse
from .schemas import AssessmentResponseCreate, AssessmentResponseUpdate
from assessments.models import Assessment, Question
from assessments.schemas import AssessmentRead


class AssessmentResponseService:
    @staticmethod
    def create_assessment_response(session: Session, response_data: AssessmentResponseCreate) -> AssessmentResponse:
        # Verify the associated assessment exists
        assessment = session.get(Assessment, response_data.assessment_id)
        if not assessment:
            raise HTTPException(status_code=404, detail="Assessment not found")

        # # Create the assessment response
        assessment_response = AssessmentResponse(
            # id=assessment_response_id,
            assessment_id=response_data.assessment_id,
            examinee_id=response_data.examinee_id,
            status=response_data.status,
            score=None
        )

        session.add(assessment_response)
        session.commit()
        session.refresh(assessment_response)
        return assessment_response

    @staticmethod
    def update_assessment_response(session: Session, response_id: int, update_data: AssessmentResponseUpdate) -> AssessmentResponse:
        assessment_response = session.get(AssessmentResponse, response_id)
        if not assessment_response:
            raise HTTPException(
                status_code=404, detail="Assessment response not found")

        # Update the fields
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(assessment_response, key, value)

        session.add(assessment_response)
        session.commit()
        session.refresh(assessment_response)
        return assessment_response

    @staticmethod
    def get_assessment_response(session: Session, response_id: int) -> AssessmentResponse:
        assessment_response = session.exec(
            select(AssessmentResponse).where(
                AssessmentResponse.id == response_id)
            .join(Assessment)
            # Eager load the assessment and question responses
            .options(
                selectinload(AssessmentResponse.assessment),
                selectinload(AssessmentResponse.question_responses)
            )
        ).first()
        if not assessment_response:
            raise HTTPException(
                status_code=404, detail="Assessment response not found")
        return assessment_response

    @staticmethod
    def list_assessment_responses(session: Session, assessment_id: int) -> List[AssessmentResponse]:
        responses = session.exec(
            select(AssessmentResponse).where(
                AssessmentResponse.assessment_id == assessment_id)
        ).all()
        return responses

    @staticmethod
    def create_question_response(session: Session, response_data: QuestionResponse, assessment_response_id: int) -> QuestionResponse:
        # Verify the associated question exists
        question = session.get(Question, response_data.question_id)
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")

        # Create the question response
        question_response = QuestionResponse(
            assessment_response_id=assessment_response_id,
            question_id=response_data.question_id,
            numeric_value=response_data.numeric_value,
            text_value=response_data.text_value
        )

        session.add(question_response)
        session.commit()
        session.refresh(question_response)
        return question_response

    @staticmethod
    def get_assessment_responses_by_examinee(session: Session, examinee_id: int) -> List[AssessmentResponse]:
        """
        Retrieve assessment responses for a specific examinee, including assessment data.
        """
        responses = (
            session.query(AssessmentResponse)
            .join(Assessment)
            .filter(AssessmentResponse.examinee_id == examinee_id)
            # Eager load the assessment
            .options(selectinload(AssessmentResponse.assessment))
            .all()
        )
        return responses

    @staticmethod
    def get_all_assessment_responses(session: Session) -> List[AssessmentResponse]:
        """
        Retrieve all assessment responses.
        """
        responses = (
            session.query(AssessmentResponse)
            .join(Assessment)
            # Eager load the assessment
            .options(selectinload(AssessmentResponse.assessment))
            .all()
        )
        return responses
