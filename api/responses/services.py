from typing import List
from pydantic import UUID4
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException
from .models import AssessmentResponse, QuestionResponse, ResponseStatus
from .schemas import AssessmentResponseCreate, AssessmentResponseRead, AssessmentResponseUpdate, BulkQuestionResponseCreate
from assessments.models import Assessment, Question


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

        # Convert SQLModel instances to dictionaries
        response_dict = assessment_response.model_dump()
        if assessment_response.assessment:
            response_dict['assessment'] = assessment_response.assessment.model_dump()

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
    def create_question_responses_bulk(session: Session, assessment_response: AssessmentResponseRead, bulk_response: BulkQuestionResponseCreate) -> AssessmentResponse:
        """
        Creates multiple question responses in bulk and calculates the total score.

        Args:
            session: The database session.
            assessment_response: The assessment response object to check the status.
            bulk_response: The bulk question response data.
            response_id: The ID of the associated assessment response.

        Returns:
            A tuple containing the total score and a list of created question responses.
        """
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

        assessment_response_saved = AssessmentResponseService.update_assessment_response_status_and_score(
            session, assessment_response, ResponseStatus.COMPLETED, total_score)
        if assessment_response_saved.status == ResponseStatus.COMPLETED:
            assessment_response.score = total_score
            assessment_response.status = ResponseStatus.COMPLETED

        return assessment_response

    @staticmethod
    def update_assessment_response_status_and_score(session: Session, assessment_response: AssessmentResponse, status_update: ResponseStatus, total_score: float = None) -> AssessmentResponse:
        """
          Updates the assessment response status and score.

          Args:
              session: The database session.
              assessment_response: Assessment Response object.
              total_score: The total score.
              status_update: The new status.
          """

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
