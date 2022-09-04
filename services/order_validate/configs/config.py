from functools import lru_cache
from dotenv import load_dotenv
from fastapi import HTTPException, status
from pydantic import BaseSettings


load_dotenv()


class Settings(BaseSettings):
    WALLET_DATABASE_URL: str
    ORDER_DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int


    class Config:
        env_file = ".env"
    

@lru_cache()
def getSettings():
    return Settings()