from datetime import datetime, timedelta
import os
from typing import Optional
from jose import jwt
from sqlmodel import Session, select
from users.models import User
from .models import TokenBlacklist

# Configuration constants
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


class AuthService:
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        from users.services import UserService
        user = UserService.get_user_by_email(db, email)
        if not user:
            return None
        if not user.verify_password(password):
            return None
        return user.model_dump() if user else None  # Convert to dict before returning

    @staticmethod
    def blacklist_token(db: Session, token: str, expires_at: datetime) -> None:
        blacklisted_token = TokenBlacklist(
            token=token,
            blacklisted_at=datetime.utcnow(),
            expires_at=expires_at
        )
        db.add(blacklisted_token)
        db.commit()

    @staticmethod
    def is_token_blacklisted(db: Session, token: str) -> bool:
        statement = select(TokenBlacklist).where(TokenBlacklist.token == token)
        result = db.exec(statement).first()
        return result is not None

    @staticmethod
    def clean_expired_tokens(db: Session) -> None:
        """Remove expired tokens from the blacklist"""
        current_time = datetime.utcnow()
        statement = select(TokenBlacklist).where(
            TokenBlacklist.expires_at < current_time)
        expired_tokens = db.exec(statement).all()
        for token in expired_tokens:
            db.delete(token)
        db.commit()
