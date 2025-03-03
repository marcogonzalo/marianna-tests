from fastapi import Request, HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import Optional


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token",
    auto_error=True
)


class OAuth2PasswordBearerOptional(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> Optional[str]:
        try:
            return await super().__call__(request)
        except HTTPException:
            return None


oauth2_scheme_optional = OAuth2PasswordBearerOptional(
    tokenUrl="/auth/token",
    auto_error=False
)
