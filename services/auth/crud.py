from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from pydantic import EmailStr
from db import database as db
from configs.config import (
        SECRET_KEY, ALGORITHM, credentialsException,
        notFoundException, ACCESS_TOKEN_EXPIRE_MINUTES)
from passlib.context import CryptContext
from schemas import TokenData, UserLogin
import json


pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2Scheme = OAuth2PasswordBearer(tokenUrl="login")


async def getUser(email: EmailStr):
    query = '''SELECT * FROM "user" WHERE email = :email'''
    return await db.fetch_one(query=query, values={"email": email})


def createAccessToken(payload: TokenData):
        toEncode = payload.dict()
        expire = datetime.utcnow() + timedelta(seconds=ACCESS_TOKEN_EXPIRE_MINUTES*60)
        toEncode.update({"exp": expire})
        toEncode["id"] = str(toEncode["id"])
        try:
            encodedJwt = jwt.encode(toEncode, SECRET_KEY, algorithm=ALGORITHM)
        except JWTError:
            raise credentialsException
        return encodedJwt


async def authenticateUser(payload: UserLogin):
        user = await getUser(payload.email)
        if not user:
            raise notFoundException
        if not verifyPassword(payload.password, user.password):
            return credentialsException
        return user 
        

def verifyPassword(plainPassword, hashedPassword):
    return pwdContext.verify(plainPassword, hashedPassword)


def encodeToJson(payload):
    return json.dumps(json.loads(payload.json())).encode("utf-8")


def decodeJson(payload: bytes):
    return json.loads(payload.decode("utf-8"))



