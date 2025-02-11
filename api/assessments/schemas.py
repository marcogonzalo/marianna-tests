from typing import Optional, List
from pydantic import BaseModel, field_validator
from datetime import datetime
from .models import ScoringMethod, ResponseStatus

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


class ChoiceRead(BaseModel):  # Change parent to BaseModel
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
    created_at: datetime
    assessment_id: int
    choices: List[ChoiceRead] = []  # Set default empty list

    @field_validator('choices')
    @classmethod
    def validate_choices(cls, v):
        # Only validate non-empty for creation, not reading
        return v

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

    @field_validator('scoring_method')
    @classmethod
    def validate_scoring_method(cls, v, info):
        values = info.data
        if v == ScoringMethod.CUSTOM:
            if values.get('min_value') is None or values.get('max_value') is None:
                raise ValueError("Custom scoring method requires explicit min_value and max_value")
        return v

class AssessmentRead(AssessmentCreate):
    id: int
    created_at: datetime
    updated_at: datetime
    questions: List[QuestionRead]

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
            raise ValueError("Either numeric_value or text_value must be provided")
        return v

class QuestionResponseRead(QuestionResponseCreate):
    id: int
    created_at: datetime
    assessment_response_id: int

class AssessmentResponseCreate(BaseModel):
    assessment_id: int
    status: ResponseStatus
    question_responses: List[QuestionResponseCreate]

class AssessmentResponseUpdate(BaseModel):
    status: ResponseStatus
    score: Optional[float] = None

class AssessmentResponseRead(BaseModel):
    id: int
    status: ResponseStatus
    score: Optional[float]
    created_at: datetime
    updated_at: datetime
    assessment_id: int
    question_responses: List[QuestionResponseRead]

class BulkQuestionResponseCreate(BaseModel):
    question_responses: List[QuestionResponseCreate]

    @field_validator('question_responses')
    @classmethod
    def validate_responses(cls, v):
        if not v:
            raise ValueError("At least one response is required")
        return v
