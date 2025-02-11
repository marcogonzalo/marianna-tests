from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship, Session, select
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
    responses: List["AssessmentResponse"] = Relationship(back_populates="assessment")

class Question(SQLModel, table=True):
    """Question model represents a question in an assessment.
    This class defines the structure and behavior of questions within assessments,
    including their relationships with assessments and choices.
    Attributes:
        id (Optional[int]): Primary key for the question.
        text (str): The actual text content of the question.
        order (int): The order/position of the question within its assessment.
        created_at (datetime): Timestamp when the question was created (UTC).
        assessment_id (int): Foreign key reference to the associated assessment.
        assessment (Assessment): Relationship to the parent assessment.
        choices (List[Choice]): List of choices associated with this question.
    Methods:
        alter_choice_list(choices: List[Choice], session: Session) -> None:
            Updates the choices list for the question, handling additions, updates, and deletions.
            Args:
                choices: List of Choice objects to update/add
                session: SQLAlchemy session for database operations
        update_choices(choices: List[Choice], session: Session) -> List[int]:
            Updates existing choices and creates new ones.
            Args:
                choices: List of Choice objects to process
                session: SQLAlchemy session for database operations
            Returns:
                List of updated choice IDs
        delete_choices(choice_ids: List[int], session: Session) -> None:
            Deletes specified choices from the database.
            Args:
                choice_ids: List of choice IDs to delete
                session: SQLAlchemy session for database operations
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    order: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Foreign keys
    assessment_id: int = Field(foreign_key="assessment.id")

    # Relationships
    assessment: Assessment = Relationship(back_populates="questions")
    choices: List["Choice"] = Relationship(
        back_populates="question",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

    # Methods
    def update_attributes(self, question_data) -> None:
        """Update question attributes from pydantic model or dict."""
        data = question_data.dict() if hasattr(question_data, 'dict') else question_data
        only_question_data = {k: v for k, v in data.items() if k != 'choices'}
        for key, value in only_question_data.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def alter_choice_list(self, choices: List["Choice"], session: Session) -> None:
        # Get existing choices IDs
        existing_choice_ids = {choice.id for choice in self.choices}
        updated_choice_ids = self.update_choices(choices, session)

        # Delete choices that are not in the update data
        choices_to_delete = existing_choice_ids - updated_choice_ids
        if choices_to_delete:
            self.delete_choices(list(choices_to_delete), session)

    def update_choices(self, choices: List["Choice"], session: Session) -> List[int]:
        updated_choice_ids = set()
        for choice_data in choices:
            # Handle both SQLModel Choice instances and ChoiceCreate schema instances
            choice_dict = choice_data.dict() if hasattr(choice_data, 'dict') else vars(choice_data)
            choice_id = getattr(choice_data, 'id', None)

            if choice_id:
                # Update existing choice
                choice = session.exec(
                    select(Choice)
                    .where(Choice.question_id == self.id)
                    .where(Choice.id == choice_id)
                ).first()
                if choice:
                    for key, value in choice_dict.items():
                        if key != 'id' and hasattr(choice, key):
                            setattr(choice, key, value)
                    updated_choice_ids.add(choice.id)
            else:
                # Create new choice
                new_choice = Choice(
                    **{k: v for k, v in choice_dict.items() if k != 'id'},
                    question_id=self.id
                )
                session.add(new_choice)
                session.commit()
                session.refresh(new_choice)
                updated_choice_ids.add(new_choice.id)

        return updated_choice_ids

    def delete_choices(self, choice_ids: List[int], session: Session) -> None:
        if choice_ids:
            # Delete choices directly using a DELETE query
            statement = Choice.__table__.delete().where(
                Choice.id.in_(choice_ids),
                Choice.question_id == self.id
            )
            session.execute(statement)


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

class ResponseStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    ABANDONED = "abandoned"

class AssessmentResponse(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    status: ResponseStatus = Field(default=ResponseStatus.PENDING)
    score: Optional[float] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Foreign keys
    assessment_id: int = Field(foreign_key="assessment.id")

    # Relationships
    assessment: Assessment = Relationship(back_populates="responses")
    question_responses: List["QuestionResponse"] = Relationship(back_populates="assessment_response")

class QuestionResponse(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    numeric_value: Optional[float] = None
    text_value: Optional[str] = Field(default=None, sa_type=Text)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Foreign keys
    question_id: int = Field(foreign_key="question.id")
    selected_choice_id: Optional[int] = Field(foreign_key="choice.id", default=None)
    assessment_response_id: int = Field(foreign_key="assessmentresponse.id")

    # Relationships
    assessment_response: AssessmentResponse = Relationship(back_populates="question_responses")
    selected_choice: Optional[Choice] = Relationship()
