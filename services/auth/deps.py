from typing import Optional

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer as BaseHTTPBearer
from pydantic import ValidationError
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession

from services.auth.crud import verifyAccessToken
from services.auth.schemas import TokenData
from services.db.deps import get_db_session
from services.user.crud import getUserById


class HTTPBearer(BaseHTTPBearer):
    async def __call__(self, request: Request) -> Optional[str]:
        credentials = await super().__call__(request)
        return credentials.credentials


reusable_oauth2 = HTTPBearer()


async def getCurrentUser(
        db: AsyncSession = Depends(get_db_session),
        token: str = Depends(reusable_oauth2)):
    try:
        payload = verifyAccessToken(token)
        schema = TokenData(**payload)
    except (ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not valid token",
        )

    user = await getUserById(db=db, id=schema.id)
    return user


async def getAdminUser(
        db: AsyncSession = Depends(get_db_session),
        token: str = Depends(reusable_oauth2)):
    try:
        payload = verifyAccessToken(token)
        schema = TokenData(**payload)
        if not schema.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough rights",
            )
    except (ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not valid token",
        )
    user = await getUserById(db=db, id=schema.id)
    return user
