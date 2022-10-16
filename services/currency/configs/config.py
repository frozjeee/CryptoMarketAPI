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
    BaseHTTPException: HTTPException = HTTPException

    class Config:
        env_file = ".env"


@lru_cache()
def getSettings():
    return Settings()
