from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: str | None = None


class Login(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(Token):
    email: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    email: str


class RefreshRequest(BaseModel):
    refresh_token: str
