from pydantic import BaseSettings
from dotenv import load_dotenv
import asyncio


load_dotenv("config/.env")


class Settings(BaseSettings):
    # database
    DATABASE_URL: str

    # JWT token
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # ID analyzer
    ID_ANALYZER_API_KEY: str
    ID_ANALYZER_REGION: str

    loop = asyncio.get_event_loop

    RABBITMQ_URL: str
    RABBITMQ_QUEUE_NAME: str
    RABBITMQ_RECONNECT_INTERVAL: int

    class Config:
        env_file = ".env"


settings = Settings()
