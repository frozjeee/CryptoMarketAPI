import time
from typing import Union, Dict, Any

from fastapi import status, HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta

from services.auth.schemas import TokenData
from config.config import settings


def createAccessToken(
    payload: dict
):
    payload = TokenData(**payload)
    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    payload["exp"] = expire
    try:
        encodedJwt = jwt.encode(
            payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error with authentication server",
        )
    return encodedJwt


def verifyAccessToken(token: str) -> Union[bool, Dict[str, Any]]:
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    return payload
