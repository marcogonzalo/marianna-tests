from typing import Optional, List
from pydantic import BaseModel, field_validator
from datetime import datetime
from .models import ScoringMethod

class ChoiceCreate(BaseModel):
    text: str
    value: float
    order: int

    @field_validator('value')
    @classmethod
    def validate_value(cls, v):
        # Additional validation could be added here based on scoring_method
        return v

class ChoiceRead(ChoiceCreate):
    id: int
    created_at: datetime
    question_id: int

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

class QuestionRead(QuestionCreate):
    id: int
    created_at: datetime
    assessment_id: int
    choices: List[ChoiceRead]

class QuestionUpdate(QuestionCreate):
    choices: List[ChoiceUpdate]

class AssessmentCreate(BaseModel):
    title: str
    description: Optional[str] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    scoring_method: ScoringMethod
    questions: Optional[List[QuestionCreate]] = None

    @field_validator('min_value', 'max_value')
    @classmethod
    def validate_values(cls, v, info):
        if v is None and info.data.get('scoring_method') == ScoringMethod.CUSTOM:
            raise ValueError("Custom scoring method requires min_value and max_value")
        if v is not None and v < 0:
            raise ValueError("Values cannot be negative")
        return v

    @field_validator('max_value')
    @classmethod
    def validate_max_value(cls, v, info):
        if v is None:
            return v
        if info.data.get('min_value') is not None and v < info.data['min_value']:
            raise ValueError("max_value must be greater than min_value")
        return v

class AssessmentRead(AssessmentCreate):
    id: int
    created_at: datetime
    updated_at: datetime
    questions: List[QuestionRead]
