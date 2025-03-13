from typing import Optional, List
from pydantic import BaseModel, field_validator, Field
from datetime import datetime, timezone
from .models import ScoringMethod
from app.utils.datetime import get_current_datetime


class ChoiceCreate(BaseModel):
    text: str
    value: float
    order: int

    @field_validator('value')
    @classmethod
    def validate_value(cls, v):
        # Additional validation could be added here based on scoring_method
        return v

    @field_validator('text')
    @classmethod
    def validate_text(cls, v):
        if not v or not isinstance(v, str):
            raise ValueError("Text must be a non-empty string")
        return v

    @field_validator('order')
    @classmethod
    def validate_order(cls, v):
        if not isinstance(v, int):
            raise ValueError("Order must be an integer")
        return v


class ChoiceRead(BaseModel):
    id: int
    text: str
    value: float
    order: int


class ChoiceUpdate(ChoiceCreate):
    id: Optional[int] = None


class QuestionCreate(BaseModel):
    text: str
    order: int
    choices: List[ChoiceCreate]

    @field_validator('choices')
    @classmethod
    def validate_choices(cls, v):
        if not v:
            raise ValueError("At least one choice is required")
        return v

    @field_validator('text')
    @classmethod
    def validate_text(cls, v):
        if not v or not isinstance(v, str):
            raise ValueError("Text must be a non-empty string")
        return v

    @field_validator('order')
    @classmethod
    def validate_order(cls, v):
        if not isinstance(v, int):
            raise ValueError("Order must be an integer")
        return v


class QuestionRead(BaseModel):
    id: int
    text: str
    order: int
    created_at: datetime = Field(default_factory=get_current_datetime)
    assessment_id: int
    choices: List[ChoiceRead] = []

    @field_validator('created_at')
    @classmethod
    def ensure_timezone(cls, v: datetime) -> datetime:
        if v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v

    @field_validator('choices')
    @classmethod
    def validate_choices(cls, v):
        # Only validate non-empty for creation, not reading
        return v


class QuestionUpdate(QuestionCreate):
    id: Optional[int]
    choices: List[ChoiceUpdate]


class AssessmentBase(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    scoring_method: ScoringMethod

    @field_validator('min_value', 'max_value')
    @classmethod
    def validate_values(cls, v, info):
        if v is None and info.data.get('scoring_method') == ScoringMethod.CUSTOM:
            raise ValueError(
                "Custom scoring method requires min_value and max_value")
        return v

    @field_validator('min_value')
    @classmethod
    def validate_min_value(cls, v, info):
        if v is None:
            return v
        if info.data.get('max_value') is not None and v < info.data['max_value']:
            raise ValueError("max_value must be greater than min_value")
        return v

    @field_validator('max_value')
    @classmethod
    def validate_max_value(cls, v, info):
        if v is None:
            return v
        if info.data.get('min_value') is not None and v < info.data['min_value']:
            raise ValueError("max_value must be greater than min_value")
        return v

    @field_validator('scoring_method')
    @classmethod
    def validate_scoring_method(cls, v, info):
        values = info.data
        if v == ScoringMethod.CUSTOM:
            if values.get('min_value') is None or values.get('max_value') is None:
                raise ValueError(
                    "Custom scoring method requires explicit min_value and max_value")
        return v

    @field_validator('scoring_method')
    @classmethod
    def set_default_values(cls, v, info):
        if v == ScoringMethod.BOOLEAN:
            info.data['min_value'] = 0.0
            info.data['max_value'] = 1.0
        if v == ScoringMethod.SCORED:
            info.data['min_value'] = -1.0
            info.data['max_value'] = 1.0
        return v


class DiagnosticCreate(BaseModel):
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    description: str


class DiagnosticRead(DiagnosticCreate):
    id: int


class AssessmentCreate(AssessmentBase):
    questions: List[QuestionCreate] = []


class AssessmentUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]


class AssessmentRead(AssessmentCreate):
    id: int
    questions: List[QuestionRead] = []
    created_at: datetime = Field(default_factory=get_current_datetime)
    updated_at: datetime = Field(default_factory=get_current_datetime)

    @field_validator('created_at', 'updated_at')
    @classmethod
    def ensure_timezone(cls, v: datetime) -> datetime:
        if v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v


class AssessmentReadWithDiagnostics(AssessmentRead):
    diagnostics: List[DiagnosticRead] = []
