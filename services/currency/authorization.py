from fastapi import status
from jose import JWTError, jwt
from schemas import TokenData
import configs.config as config


def validateToken(
    token: str,
    settings: config.Settings = config.getSettings()):
    if not token:
        raise settings.BaseHTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No authentication token provided"
        )
    token = token.split(" ")[1]
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        tokenData = TokenData.parse_obj(payload)
    except JWTError:
        raise settings.BaseHTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication  token no longer valid",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return tokenData
