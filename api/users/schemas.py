from datetime import datetime, timezone
from pydantic import BaseModel, EmailStr, UUID4, Field, field_validator
from typing import Optional
from .enums import UserRole
from utils.datetime import get_current_datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserAccountCreate(BaseModel):
    email: EmailStr
    password: str
    account: Optional["AccountCreate"]


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None


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


class AccountUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[UserRole] = None


class AccountRead(BaseModel):
    id: UUID4
    first_name: str
    last_name: str
    role: UserRole
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
