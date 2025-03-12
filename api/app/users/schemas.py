from datetime import date, datetime, timedelta, timezone
from pydantic import BaseModel, EmailStr, UUID4, Field, field_validator
from typing import Optional
from .enums import Gender, UserRole
from app.utils.datetime import get_current_datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserAccountCreate(BaseModel):
    email: EmailStr
    password: str
    account: Optional["AccountCreate"] = None


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    account: Optional["AccountCreate"] = None


class UserRead(BaseModel):
    id: UUID4
    email: EmailStr
    created_at: datetime = Field(default_factory=get_current_datetime)
    updated_at: datetime = Field(default_factory=get_current_datetime)
    account: Optional["AccountRead"] = None

    @field_validator('created_at', 'updated_at')
    @classmethod
    def ensure_timezone(cls, v: datetime) -> datetime:
        if v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v

    class Config:
        from_attributes = True


class AccountCreate(BaseModel):
    first_name: str
    last_name: str
    role: UserRole

    @field_validator('first_name', 'last_name')
    @classmethod
    def validate_names(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Name fields cannot be empty")
        return v.strip()


class AccountUpdate(AccountCreate):
    pass


class AccountRead(AccountCreate):
    id: UUID4
    user_id: UUID4
    created_at: datetime = Field(default_factory=get_current_datetime)
    updated_at: datetime = Field(default_factory=get_current_datetime)

    @field_validator('created_at', 'updated_at')
    @classmethod
    def ensure_timezone(cls, v: datetime) -> datetime:
        if v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v

    class Config:
        from_attributes = True


class ExamineeBase(BaseModel):
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    birth_date: date  # Use str for date in Pydantic
    gender: Gender
    email: EmailStr
    internal_identifier: Optional[str]
    comments: Optional[str]

    @field_validator('first_name', 'last_name')
    @classmethod
    def validate_names(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Name fields cannot be empty")
        return v.strip()


class ExamineeCreate(ExamineeBase):
    created_by: Optional[UUID4] = None


class ExamineeUpdate(ExamineeBase):
    pass


class ExamineeRead(ExamineeBase):
    id: UUID4
    created_by: UUID4  # This should link to the Account model
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
