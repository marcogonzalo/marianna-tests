from typing import Optional, List
from pydantic import UUID4
from sqlmodel import SQLModel, Field, Relationship, Text, DateTime
from datetime import datetime, timezone
from enum import Enum
from assessments.models import Assessment, Choice
from users.models import Examinee
from utils.datetime import get_current_datetime


class ResponseStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


class AssessmentResponse(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    status: ResponseStatus = Field(default=ResponseStatus.PENDING)
    score: Optional[float] = None
    created_at: datetime = Field(
        default_factory=get_current_datetime,
        sa_type=DateTime(timezone=True)
    )
    updated_at: datetime = Field(
        default_factory=get_current_datetime,
        sa_type=DateTime(timezone=True)
    )

    # Foreign keys
    assessment_id: int = Field(foreign_key="assessment.id")
    examinee_id: UUID4 = Field(foreign_key="examinee.id", nullable=False)

    # Relationships
    assessment: Assessment = Relationship(back_populates="responses")
    question_responses: List["QuestionResponse"] = Relationship(
        back_populates="assessment_response")
    examinee: "Examinee" = Relationship(back_populates="assessment_responses")

    def __init__(self, **data):
        """
        Initialize AssessmentResponse with timezone-aware datetime fields.
        Ensures created_at and updated_at fields have UTC timezone info
        when instances are created.
        """
        super().__init__(**data)
        if self.created_at and self.created_at.tzinfo is None:
            self.created_at = self.created_at.replace(tzinfo=timezone.utc)
        if self.updated_at and self.updated_at.tzinfo is None:
            self.updated_at = self.updated_at.replace(tzinfo=timezone.utc)


class QuestionResponse(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    numeric_value: Optional[float] = None
    text_value: Optional[str] = Field(default=None, sa_type=Text)
    created_at: datetime = Field(
        default_factory=get_current_datetime,
        sa_type=DateTime(timezone=True)
    )

    # Foreign keys
    question_id: int = Field(foreign_key="question.id")
    selected_choice_id: Optional[int] = Field(
        foreign_key="choice.id", default=None)
    assessment_response_id: int = Field(foreign_key="assessmentresponse.id")

    # Relationships
    assessment_response: AssessmentResponse = Relationship(
        back_populates="question_responses")
    selected_choice: Optional[Choice] = Relationship()

    def __init__(self, **data):
        """
        Initialize QuestionResponse with timezone-aware datetime fields.
        Ensures created_at field has UTC timezone info when instances are created.
        """
        super().__init__(**data)
        if self.created_at and self.created_at.tzinfo is None:
            self.created_at = self.created_at.replace(tzinfo=timezone.utc)
