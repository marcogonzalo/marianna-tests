from datetime import datetime
from sqlmodel import SQLModel, Field, DateTime
from typing import Optional


class TokenBlacklist(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    token: str = Field(index=True)
    blacklisted_at: datetime = Field(sa_type=DateTime(timezone=True))
    expires_at: datetime = Field(sa_type=DateTime(timezone=True))
