from functools import lru_cache
from dotenv import load_dotenv
from fastapi import HTTPException
from pydantic import BaseSettings


load_dotenv("configs/.env")



class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    BaseHTTPException:HTTPException =  HTTPException
    

    class Config:
        env_file = ".env"


@lru_cache()
def getSettings():
    return Settings()

# notFoundException = HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail="User not found",
#     )

# credentialsException = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )

# forbiddenException = HTTPException(
#         status_code=status.HTTP_403_FORBIDDEN,
#         detail="Not enough rights",
#     )
