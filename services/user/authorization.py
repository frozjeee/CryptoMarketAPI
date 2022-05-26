from datetime import datetime
from jose import JWTError, jwt
from db import database as db
from configs.config import (SECRET_KEY, ALGORITHM, 
    credentialsException, forbiddenException,
    unauthorizedException)
from schemas import TokenData
from passlib.context import CryptContext


pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
    

def validateToken(token: str):
    if not token:
        raise unauthorizedException
    token = token.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        tokenData = TokenData.parse_obj(payload)
    except JWTError:
        raise credentialsException
    return tokenData