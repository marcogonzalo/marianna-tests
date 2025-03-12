import os
from typing import List
from pydantic import UUID4
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException

from app.users.schemas import ExamineeRead, UserRead
from app.email_sender.services import EmailSender
from app.users.models import Examinee, User
from .models import AssessmentResponse, QuestionResponse, ResponseStatus
from .schemas import AssessmentResponseCreate, AssessmentResponseRead, AssessmentResponseUpdate, BulkQuestionResponseCreate
from app.assessments.models import Assessment, Question


class AssessmentResponseService:
    @staticmethod
    def create_assessment_response(session: Session, response_data: AssessmentResponseCreate) -> AssessmentResponse:
        # Verify the associated assessment exists
        assessment = session.get(Assessment, response_data.assessment_id)
        if not assessment:
            raise HTTPException(status_code=404, detail="Assessment not found")

        # # Create the assessment response
        assessment_response = AssessmentResponse(
            assessment_id=response_data.assessment_id,
            examinee_id=response_data.examinee_id,
            status=response_data.status,
            created_by=response_data.created_by,
            score=None
        )

        session.add(assessment_response)
        session.commit()
        session.refresh(assessment_response)
        return assessment_response

    @staticmethod
    def update_assessment_response(session: Session, response_id: str, update_data: AssessmentResponseUpdate) -> AssessmentResponse:
        assessment_response = session.get(AssessmentResponse, response_id)
        if not assessment_response:
            raise HTTPException(
                status_code=404, detail="Assessment response not found")

        # Update the fields
        for key, value in update_data.items():
            setattr(assessment_response, key, value)

        session.add(assessment_response)
        session.commit()
        session.refresh(assessment_response)
        return assessment_response

    @staticmethod
    def get_assessment_response(session: Session, response_id: str) -> AssessmentResponse:
        assessment_response = session.exec(
            select(AssessmentResponse).where(
                AssessmentResponse.id == response_id)
            .join(Assessment)
            .options(
                selectinload(AssessmentResponse.assessment),
                selectinload(AssessmentResponse.question_responses)
            )
        ).first()
        if not assessment_response:
            raise HTTPException(
                status_code=404, detail="Assessment response not found")

        # Convert SQLModel instances to dictionaries
        response_dict = assessment_response.model_dump()
        if assessment_response.assessment:
            response_dict['assessment'] = assessment_response.assessment.model_dump()
        if assessment_response.question_responses:
            response_dict['question_responses'] = [
                qr.model_dump() for qr in assessment_response.question_responses
            ]

        return response_dict

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

    @staticmethod
    def create_question_responses_bulk(session: Session, assessment_response_id: str, bulk_response: BulkQuestionResponseCreate) -> AssessmentResponse:
        """
        Creates multiple question responses in bulk and calculates the total score.
        """
        # Get the actual database model instance
        assessment_response = session.get(
            AssessmentResponse, assessment_response_id)
        if not assessment_response:
            raise HTTPException(
                status_code=404, detail="Assessment response not found")

        if assessment_response.status != ResponseStatus.PENDING:
            raise HTTPException(
                status_code=400, detail="Cannot process responses; the assessment is not in a PENDING state.")

        question_responses = []
        total_score = 0

        for response_data in bulk_response.question_responses:
            question_response = AssessmentResponseService.create_question_response(
                session, response_data, assessment_response.id)

            if response_data.numeric_value is not None:
                total_score += response_data.numeric_value

            question_responses.append(question_response)

        assessment_response = AssessmentResponseService.update_assessment_response_status_and_score(
            session, assessment_response.id, ResponseStatus.COMPLETED, total_score)

        return assessment_response

    @staticmethod
    def update_assessment_response_status_and_score(session: Session, response_id: str, status_update: ResponseStatus, total_score: float = None) -> AssessmentResponse:
        """
        Updates the assessment response status and score.
        """
        assessment_response = session.get(AssessmentResponse, response_id)
        if not assessment_response:
            raise HTTPException(
                status_code=404, detail="Assessment response not found")

        score_change = assessment_response.status == ResponseStatus.PENDING and status_update == ResponseStatus.COMPLETED and total_score is not None
        if score_change:
            assessment_response.score = total_score
        else:
            if AssessmentResponseService.is_status_change_invalid(assessment_response.status, status_update):
                raise HTTPException(
                    status_code=400, detail=f"Cannot change status from {assessment_response.status} to {status_update}")

        assessment_response.status = status_update
        session.add(assessment_response)
        session.commit()
        session.refresh(assessment_response)

        return assessment_response

    @staticmethod
    def is_status_change_invalid(current_status: ResponseStatus, new_status: ResponseStatus) -> bool:
        """
        Validate that a status change is not allowed.
        """
        allowed_transitions = {
            ResponseStatus.PENDING: [ResponseStatus.ABANDONED, ResponseStatus.DISCARDED],
            ResponseStatus.COMPLETED: [ResponseStatus.DISCARDED],
            ResponseStatus.ABANDONED: [ResponseStatus.PENDING, ResponseStatus.DISCARDED],
            ResponseStatus.DISCARDED: [ResponseStatus.PENDING],
        }

        return new_status not in allowed_transitions.get(current_status, [])

    @staticmethod
    async def send_link_by_email(response: AssessmentResponseRead, examinee: ExamineeRead, current_user: UserRead) -> dict:
        subject = f"Dr Jayaro needs you to complete the following questionnaire"
        link = f"{os.getenv('CLIENT_URL')}/public/726573706f6e7365/{response.id}/70726976617465"
        content = f"""
            <p>Dear {examinee.first_name},</p>
            <p>Dr Jayaro needs you to complete the following questionnaire in relation to your ASD assessment.</p>
            <p><a href="{link}">{link}</a></p>
            <p>The link would be active for 24 hours.</p>
            <p>If you have any doubts please do not hesitate to ask the clinic.</p>
            <hr/>
            <p>Kind regards,</p>
            <p>The Hazelton Clinic Team</p>
        """
        return await EmailSender.send_email(
            sender=current_user.email,
            receivers=examinee.email,
            subject=subject,
            content=content
        )


    @staticmethod
    async def notify_examinee_completed_assessment(response: AssessmentResponseRead, examinee: ExamineeRead, user: UserRead) -> AssessmentResponse:
        subject = f"Dr Jayaro needs you to complete the following questionnaire"
        link = f"{os.getenv('CLIENT_URL')}/responses/{response.id}"
        content = f"""
            <p>Hello,</p>
            <p>The questionnaire has been completed by {examinee.first_name} {examinee.last_name}.</p>
            <p>Now, you can go to the app to see the results here: <a href="{link}">{link}</a></p>
            <hr/>
            <p>Regards,</p>
            <p>The Hazelton Clinic Team</p>
        """
        return await EmailSender.send_email(
            sender=user.email,
            receivers=examinee.email,
            subject=subject,
            content=content
        )