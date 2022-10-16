from fastapi.security import OAuth2PasswordBearer
from fastapi import status

from jose import JWTError, jwt

from datetime import datetime, timedelta
from pydantic import EmailStr

from db import database as db

from passlib.context import CryptContext
from schemas import TokenData, UserLogin

import configs.config as config


pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2Scheme = OAuth2PasswordBearer(tokenUrl="login")


async def getUser(email: EmailStr):
    query = '''SELECT * FROM "user" WHERE email = :email'''
    return await db.fetch_one(query=query, values={"email": email})


def createAccessToken(
        payload: TokenData,
        settings: config.Settings = config.getSettings()
):

    toEncode = payload.dict()
    expire = datetime.utcnow() + timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE_MINUTES*60)
    toEncode.update({"exp": expire})
    toEncode["id"] = str(toEncode["id"])
    try:
        encodedJwt = jwt.encode(toEncode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    except JWTError:
        raise settings.BaseHTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error with authentication server")
    return encodedJwt


async def authenticateUser(
        payload: UserLogin,
        settings: config.Settings = config.getSettings()
):

    user = await getUser(payload.email)

    if not user:
        raise settings.BaseHTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User does not exist")

    if not verifyPassword(payload.password, user.password):
        raise settings.BaseHTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Wrong password")

    return user


def verifyPassword(plainPassword, hashedPassword):
    return pwdContext.verify(plainPassword, hashedPassword)
