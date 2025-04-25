from typing import Optional, List
from pydantic import UUID4, BaseModel, field_validator, Field
from datetime import datetime, timezone

from app.assessments.schemas import AssessmentBase, AssessmentRead

from .models import ResponseStatus
from app.utils.datetime import get_current_datetime


class AssessmentResponseCreate(BaseModel):
    assessment_id: int
    status: ResponseStatus = ResponseStatus.PENDING
    examinee_id: UUID4
    created_by: UUID4


class AssessmentResponseUpdate(BaseModel):
    status: ResponseStatus
    score: Optional[float] = None


class AssessmentResponseRead(AssessmentResponseCreate):
    id: str
    score: Optional[float] = None
    created_at: datetime = Field(default_factory=get_current_datetime)
    updated_at: datetime = Field(default_factory=get_current_datetime)

    class Config:
        from_attributes = True
        from_attributes = True

    @field_validator('created_at', 'updated_at')
    @classmethod
    def ensure_timezone(cls, v: datetime) -> datetime:
        if v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v


class AssessmentResponseReadWithAssessment(AssessmentResponseRead):
    id: str
    score: Optional[float] = None
    assessment: Optional[AssessmentBase]
    examinee_id: UUID4 | str


class AssessmentResponseReadWithQuestions(AssessmentResponseReadWithAssessment):
    id: str
    status: ResponseStatus
    score: Optional[float]
    assessment: AssessmentRead
    question_responses: List["QuestionResponseRead"] = []

    class Config:
        from_attributes = True


class BulkQuestionResponseCreate(BaseModel):
    question_responses: List["QuestionResponseCreate"]

    @field_validator('question_responses')
    @classmethod
    def validate_responses(cls, v):
        if not v:
            raise ValueError("At least one response is required")
        return v


class QuestionResponseCreate(BaseModel):
    numeric_value: Optional[float] = None
    text_value: Optional[str] = None
    question_id: int

    @field_validator('numeric_value', 'text_value')
    @classmethod
    def validate_value_present(cls, v, info):
        # Get the other value from the current validation context
        if info.field_name == 'numeric_value':
            other_value = info.data.get('text_value')
        else:
            other_value = info.data.get('numeric_value')

        # If both the current value and the other value are None, raise error
        if v is None and other_value is None:
            raise ValueError(
                "Either numeric_value or text_value must be provided")
        return v


class QuestionResponseRead(QuestionResponseCreate):
    id: int
    created_at: datetime = Field(default_factory=get_current_datetime)
    assessment_response_id: str

    @field_validator('created_at')
    @classmethod
    def ensure_timezone(cls, v: datetime) -> datetime:
        if v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v


class AssessmentResponseCreateParams(BaseModel):
    examinee_id: UUID4
