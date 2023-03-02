import jwt

from typing import Optional

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer as BaseHTTPBearer
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from starlette import status
from passlib.context import CryptContext

from services.auth.crud import verifyAccessToken
from services.auth.schemas import TokenData
from services.user.crud import getUserById


pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2Scheme = OAuth2PasswordBearer(tokenUrl="login")


class HTTPBearer(BaseHTTPBearer):
    async def __call__(self, request: Request) -> Optional[str]:
        credentials = await super().__call__(request)
        return credentials.credentials


reusable_oauth2 = HTTPBearer()


async def getCurrentUser(token: str = Depends(reusable_oauth2)):
    try:
        payload = verifyAccessToken(token)
        schema = TokenData(**payload)
    except (jwt.InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not valid token",
        )

    user = await getUserById(userId=schema.id)
    return user


async def getAdminUser(token: str = Depends(reusable_oauth2)):
    try:
        payload = verifyAccessToken(token)
        schema = TokenData(**payload)
        if not schema.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough rights",
            )
    except (jwt.InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not valid token",
        )
    user = await getUserById(userId=schema.id)
    return user
