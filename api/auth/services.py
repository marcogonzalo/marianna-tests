from datetime import datetime, timedelta
import os
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlmodel import Session, select
from database import get_session
from users.models import User
from .models import TokenBlacklist
from .schemas import TokenData
from .security import oauth2_scheme

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
    def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
        from users.services import UserService
        user = UserService.get_user_by_email(session, email)
        if not user:
            return None
        if not user.verify_password(password):
            return None
        return user.model_dump() if user else None  # Convert to dict before returning

    @staticmethod
    def blacklist_token(session: Session, token: str, expires_at: datetime) -> None:
        blacklisted_token = TokenBlacklist(
            token=token,
            blacklisted_at=datetime.utcnow(),
            expires_at=expires_at
        )
        session.add(blacklisted_token)
        session.commit()

    @staticmethod
    def is_token_blacklisted(session: Session, token: str) -> bool:
        statement = select(TokenBlacklist).where(TokenBlacklist.token == token)
        result = session.exec(statement).first()
        return result is not None

    @staticmethod
    def clean_expired_tokens(session: Session) -> None:
        """Remove expired tokens from the blacklist"""
        current_time = datetime.utcnow()
        statement = select(TokenBlacklist).where(
            TokenBlacklist.expires_at < current_time)
        expired_tokens = session.exec(statement).all()
        for token in expired_tokens:
            session.delete(token)
        session.commit()

    @staticmethod
    def get_current_user_from_token(
        token: str = Depends(oauth2_scheme),
        session: Session = Depends(get_session)
    ):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        if token is None or AuthService.is_token_blacklisted(session, token):
            raise credentials_exception

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            exp: int = payload.get("exp")

            if email is None:
                raise credentials_exception

            # Check token expiration
            if datetime.utcfromtimestamp(exp) < datetime.utcnow():
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            token_data = TokenData(email=email)
        except JWTError:
            raise credentials_exception

        from users.services import UserService
        user = UserService.get_user_by_email(session, email=token_data.email)
        if user is None:
            raise credentials_exception

        return user

    @staticmethod
    async def get_current_user(
        current_user=Depends(get_current_user_from_token)
    ):
        return current_user

    @staticmethod
    async def get_current_active_user(
        current_user=Depends(get_current_user)
    ):
        user = await current_user
        if user.deleted_at is not None:
            raise HTTPException(status_code=400, detail="Inactive user")
        return user
