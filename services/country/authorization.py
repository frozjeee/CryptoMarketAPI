from jose import JWTError, jwt
from configs.config import (
    SECRET_KEY,
    ALGORITHM,
    credentialsException,
    unauthorizedException
)
from schemas import TokenData


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
