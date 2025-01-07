from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from enum import Enum
from sqlalchemy import Text

class ScoringMethod(str, Enum):
    BOOLEAN = "boolean"  # Simple true/false, adds 1 or 0
    SCORED = "scored"    # Custom scores with possible penalties
    CUSTOM = "custom"    # User-defined min and max values

class Assessment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str  
    description: Optional[str] = Field(default=None, sa_type=Text)
    min_value: float
    max_value: float
    scoring_method: ScoringMethod
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    def set_default_values(self) -> None:
        if self.scoring_method == ScoringMethod.BOOLEAN:
            self.min_value = 0
            self.max_value = 1
        elif self.scoring_method == ScoringMethod.SCORED:
            self.min_value = -1
            self.max_value = 1
        elif self.scoring_method == ScoringMethod.CUSTOM:
            raise ValueError("Custom scoring method requires explicit min_value and max_value")
    
    # Relationships
    questions: List["Question"] = Relationship(back_populates="assessment")

class Question(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    order: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Foreign keys
    assessment_id: int = Field(foreign_key="assessment.id")
    
    # Relationships
    assessment: Assessment = Relationship(back_populates="questions")
    choices: List["Choice"] = Relationship(back_populates="question")

class Choice(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    value: float  # For BOOLEAN: 0 or 1, for SCORED: any value between min_value and max_value
    order: int    # Display order in the UI
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Foreign keys
    question_id: int = Field(foreign_key="question.id")
    
    # Relationships
    question: Question = Relationship(back_populates="choices")
