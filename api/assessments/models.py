from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from enum import Enum

class ScoringMethod(str, Enum):
    BOOLEAN = "boolean"  # Simple true/false, adds 1 or 0
    SCORED = "scored"    # Custom scores with possible penalties
    RANKING = "ranking"  # Ordered options from best to worst

class Assessment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    min_value: float
    max_value: float
    scoring_method: ScoringMethod
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    questions: List["Question"] = Relationship(back_populates="assessment")

class Question(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    weight: float = Field(default=1.0)
    order: int
    scoring_method: Optional[ScoringMethod] = Field(default=ScoringMethod.BOOLEAN)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Foreign keys
    assessment_id: int = Field(foreign_key="assessment.id")
    
    # Relationships
    assessment: Assessment = Relationship(back_populates="questions")
    options: List["AnswerOption"] = Relationship(back_populates="question")

class AnswerOption(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    value: float  # For BOOLEAN: 0 or 1, for SCORED: any value, for RANKING: position (1,2,3,...)
    order: int    # Display order in the UI
    is_correct: bool = Field(default=False)  # Particularly useful for BOOLEAN scoring
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Foreign keys
    question_id: int = Field(foreign_key="question.id")
    
    # Relationships
    question: Question = Relationship(back_populates="options")
