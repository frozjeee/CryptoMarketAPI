from functools import lru_cache
from dotenv import load_dotenv
from pydantic import BaseSettings


load_dotenv("config/.env")


class Settings(BaseSettings):
    COUNTRY_DATABASE_URL: str
    CURRENCY_DATABASE_URL: str
    WALLET_DATABASE_URL: str
    USER_DATABASE_URL: str
    TRANSACTION_DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"


@lru_cache()
def getSettings():
    return Settings()
