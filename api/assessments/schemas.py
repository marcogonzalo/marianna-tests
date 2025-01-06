from typing import Optional, List
from pydantic import BaseModel, field_validator
from datetime import datetime
from .models import ScoringMethod

class AnswerOptionCreate(BaseModel):
    text: str
    value: float
    order: int
    is_correct: bool = False

    @field_validator('value')
    @classmethod
    def validate_value(cls, v):
        # Additional validation could be added here based on scoring_method
        return v

class AnswerOptionRead(AnswerOptionCreate):
    id: int
    created_at: datetime
    question_id: int

class QuestionCreate(BaseModel):
    text: str
    weight: Optional[float] = 1.0
    order: int
    scoring_method: Optional[ScoringMethod] = None
    options: List[AnswerOptionCreate]

    @field_validator('options')
    @classmethod
    def validate_options(cls, v):
        if not v:
            raise ValueError("At least one answer option is required")
        return v

class QuestionRead(QuestionCreate):
    id: int
    created_at: datetime
    assessment_id: int
    options: List[AnswerOptionRead]

class AssessmentCreate(BaseModel):
    title: str
    description: str
    min_value: float
    max_value: float
    scoring_method: ScoringMethod
    questions: Optional[List[QuestionCreate]] = None

    @field_validator('min_value', 'max_value')
    @classmethod
    def validate_values(cls, v):
        if v < 0:
            raise ValueError("Values cannot be negative")
        return v

    @field_validator('max_value')
    @classmethod
    def validate_max_value(cls, v, info):
        if info.data.get('min_value') is not None and v < info.data['min_value']:
            raise ValueError("max_value must be greater than min_value")
        return v

class AssessmentRead(AssessmentCreate):
    id: int
    created_at: datetime
    updated_at: datetime
    questions: List[QuestionRead]
