import time

from fastapi import status, HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta

from services.user.models import User
from services.auth.schemas import TokenData
from config.config import settings


def createAccessToken(
    user: User
):
    payload = TokenData(**user.__dict__)
    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    payload.__dict__.update({'exp': time.mktime(expire.timetuple())})
    try:
        encodedJwt = jwt.encode(
            payload.dict(), settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error with authentication server",
        )
    return encodedJwt


def verifyAccessToken(token: str):
    payload = jwt.decode(token, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM)
    return payload
