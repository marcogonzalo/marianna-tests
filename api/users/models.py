from pydantic import UUID4, EmailStr
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from uuid import uuid4
from .enums import UserRole
from utils.datetime import get_current_datetime
from sqlalchemy import DateTime

class User(SQLModel, table=True):
    id: UUID4 = Field(default_factory=uuid4, primary_key=True)  # Changed from id to uuid
    email: EmailStr = Field(unique=True, nullable=False)
    password_hash: str = Field(nullable=False)
    created_at: datetime = Field(
        default_factory=get_current_datetime,
        sa_type=DateTime(timezone=True)
    )
    updated_at: datetime = Field(
        default_factory=get_current_datetime,
        sa_type=DateTime(timezone=True)
    )

    account: "Account" = Relationship(back_populates="user")

    def __init__(self, **data):
        """
        Initialize User with timezone-aware datetime fields.
        Ensures created_at and updated_at fields have UTC timezone info
        when instances are created.
        """
        super().__init__(**data)
        if self.created_at and self.created_at.tzinfo is None:
            self.created_at = self.created_at.replace(tzinfo=timezone.utc)
        if self.updated_at and self.updated_at.tzinfo is None:
            self.updated_at = self.updated_at.replace(tzinfo=timezone.utc)

class Account(SQLModel, table=True):
    id: UUID4 = Field(default_factory=uuid4, primary_key=True)
    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)
    role: UserRole = Field(nullable=False)
    user_id: UUID4 = Field(foreign_key="user.id", unique=True, nullable=False)  # Changed from users.id to user.id
    created_at: datetime = Field(
      default_factory=get_current_datetime,
        sa_type=DateTime(timezone=True)
    )
    updated_at: datetime = Field(default_factory=get_current_datetime,
        sa_type=DateTime(timezone=True)
    )

    user: User = Relationship(back_populates="account")
