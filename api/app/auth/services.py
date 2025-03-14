from datetime import datetime, timedelta
import os
from typing import List, Optional
from fastapi import Depends, HTTPException, logger, status
from jose import JWTError, jwt
from sqlmodel import Session, select
from database import get_session
from app.utils.email import send_email
from app.utils.common import generate_client_url
from app.users.enums import UserRole
from app.users.models import User
from app.users.services import UserService
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
        from app.users.services import UserService
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

        from app.users.services import UserService
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
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
        return user
    
    @staticmethod
    async def get_current_assessment_developer_user(
        current_user=Depends(get_current_active_user)
    ):
        user = await current_user
        if not user.account:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden: User has no associated account"
            )
        if user.account.role != UserRole.ASSESSMENT_DEVELOPER:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden: Only assessment developers can perform this action"
            )
        return user
    
    @staticmethod
    def send_reset_password_email(session: Session, email: str) -> None:
        token = UserService.create_password_reset_token(session, email)
        if token:
            subject = "Password Reset Request"
            link = generate_client_url(f"/reset-password?token={token}")
            email_content = f"""
            <p>Hello,</p>
            <p>You have requested to reset your password. Please click the link below to set a new password:</p>
            <p><a href="{link}">{link}</a></p>
            <p>This link will expire in 4 hours.</p>
            <p>If you did not request this password reset, please ignore this email.</p>
            """
            send_email(
                recipients=email,
                subject=subject,
                content=email_content
            )


class RoleChecker:
    def __init__(self, allowed_roles: List):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(AuthService.get_current_active_user)):
        if not user.account:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden: User has no associated account"
            )
        if user.account.role not in self.allowed_roles:
            logger.logger.debug(f"User with role {user.account.role} not in {self.allowed_roles}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action."
            )
        