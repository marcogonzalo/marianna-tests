from typing import Optional, List
from pydantic import UUID4, BaseModel, field_validator, Field
from datetime import datetime, timezone

from assessments.schemas import QuestionResponseCreate, QuestionResponseRead
from .models import ResponseStatus
from utils.datetime import get_current_datetime


class AssessmentResponseCreate(BaseModel):
    assessment_id: int
    status: ResponseStatus
    examinee_id: UUID4


class AssessmentResponseUpdate(BaseModel):
    status: ResponseStatus
    score: Optional[float] = None


class AssessmentResponseRead(BaseModel):
    id: int
    status: ResponseStatus
    score: Optional[float]
    created_at: datetime = Field(default_factory=get_current_datetime)
    updated_at: datetime = Field(default_factory=get_current_datetime)
    assessment_id: int
    question_responses: List[QuestionResponseRead]
    examinee_id: UUID4

    @field_validator('created_at', 'updated_at')
    @classmethod
    def ensure_timezone(cls, v: datetime) -> datetime:
        if v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v


class BulkQuestionResponseCreate(BaseModel):
    question_responses: List[QuestionResponseCreate]

    @field_validator('question_responses')
    @classmethod
    def validate_responses(cls, v):
        if not v:
            raise ValueError("At least one response is required")
        return v
