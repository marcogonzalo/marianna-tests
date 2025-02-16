from typing import Optional
from pydantic import UUID4, EmailStr
from sqlmodel import SQLModel, Field, Relationship, DateTime, Text
from datetime import date, datetime, timezone
from uuid import uuid4
from .enums import Gender, UserRole
from utils.datetime import get_current_datetime


class User(SQLModel, table=True):
    id: UUID4 = Field(default_factory=uuid4, primary_key=True)
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
    deleted_at: datetime | None = Field(
        default=None,
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
    user_id: UUID4 = Field(foreign_key="user.id", unique=True, nullable=False)
    created_at: datetime = Field(
        default_factory=get_current_datetime,
        sa_type=DateTime(timezone=True)
    )
    updated_at: datetime = Field(default_factory=get_current_datetime,
                                 sa_type=DateTime(timezone=True)
                                 )

    user: User = Relationship(back_populates="account")


class Examinee(SQLModel, table=True):
    # __tablename__ = 'examinees'

    id: UUID4 = Field(default_factory=uuid4, primary_key=True)
    first_name: str = Field(nullable=False)
    middle_name: Optional[str] = Field(nullable=True)
    last_name: str = Field(nullable=False)
    birth_date: date = Field(nullable=False)
    gender: Gender = Field(nullable=False)
    email: EmailStr = Field(unique=True, nullable=False)
    internal_identifier: Optional[str] = Field(nullable=False)
    comments: Optional[str] = Field(sa_type=Text, nullable=True)
    created_by: UUID4 = Field(foreign_key="account.id",
                              unique=True, nullable=False)
    created_at: datetime = Field(
        default_factory=get_current_datetime,
        sa_type=DateTime(timezone=True)
    )
    updated_at: datetime = Field(
        default_factory=get_current_datetime,
        sa_type=DateTime(timezone=True)
    )
    deleted_at: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True)
    )

    # Relationship to Account model
    creator: Account = Relationship()

    # class Config:
    #     arbitrary_types_allowed=True
