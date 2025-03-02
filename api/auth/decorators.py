from fastapi import Depends
from functools import wraps
from sqlmodel import Session
from database import get_session
from .security import oauth2_scheme


def requires_auth(func):
    """Decorator to add authentication requirement to endpoints"""
    from .services import AuthService

    @wraps(func)
    async def wrapper(*args, token: str = Depends(oauth2_scheme), session: Session = Depends(get_session), **kwargs):
        AuthService.get_current_user_from_token(token, session)
        return await func(*args, token=token, session=session, **kwargs)
    return wrapper
