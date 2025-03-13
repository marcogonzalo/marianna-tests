from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlmodel import Session
from app.users.schemas import PasswordResetConfirm, PasswordResetRequest
from app.users.services import UserService
from database import get_session
from .schemas import LoginResponse, TokenResponse, RefreshRequest
from .services import AuthService, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from .security import oauth2_scheme


auth_router = APIRouter(prefix="/auth", tags=["auth"])


# Public endpoint - no authentication required
@auth_router.post("/token", response_model=LoginResponse)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    user = AuthService.authenticate_user(
        session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = AuthService.create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "email": user["email"]
    }


# Protected endpoint - requires authentication
@auth_router.post("/logout")
async def logout(
    session: Session = Depends(get_session), token=Depends(oauth2_scheme)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        expires_at = datetime.fromtimestamp(payload.get("exp"))
        AuthService.blacklist_token(session, token, expires_at)
        return {"message": "Successfully logged out"}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )


# Protected endpoint - requires authentication
@auth_router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_token: RefreshRequest,
    session: Session = Depends(get_session), current_user=Depends(AuthService.get_current_active_user)
):
    try:
        payload = jwt.decode(refresh_token.refresh_token,
                             SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user = UserService.get_user_by_email(session, email=email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expires = timedelta(days=7)

        new_access_token = AuthService.create_access_token(
            data={"sub": email},
            expires_delta=access_token_expires
        )
        new_refresh_token = AuthService.create_access_token(
            data={"sub": email},
            expires_delta=refresh_token_expires
        )

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
            "email": email
        }
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

@auth_router.post("/reset-password/request")
async def request_password_reset(
    request_data: PasswordResetRequest,
    session: Session = Depends(get_session)
):
    
    user = UserService.get_user_by_email(session, request_data.email)
    if user:
        AuthService.send_reset_password_email(session, user.email)
    
    # Always return success to prevent email enumeration
    return {"message": "If the email exists, a password reset link has been sent"}


@auth_router.post("/reset-password/confirm")
async def confirm_password_reset(
    reset_data: PasswordResetConfirm,
    session: Session = Depends(get_session)
):
    if UserService.reset_password(session, reset_data.token, reset_data.password):
        return {"message": "Password has been reset successfully"}
    return {"message": "Invalid or expired token"}