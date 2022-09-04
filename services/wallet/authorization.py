from fastapi import Depends
from jose import JWTError, jwt
from schemas import TokenData
from passlib.context import CryptContext
import configs.config as config


pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
    

def validateToken(token: str, settings: config.Settings = Depends(config.getSettings)):
    if not token:
        raise settings.unauthorizedException
    token = token.split(" ")[1]
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        tokenData = TokenData.parse_obj(payload)
    except JWTError:
        raise settings.credentialsException
    return tokenData