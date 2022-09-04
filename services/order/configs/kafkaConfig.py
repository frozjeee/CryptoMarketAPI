import asyncio
from functools import lru_cache
from dotenv import load_dotenv
from pydantic import BaseSettings


load_dotenv("configs/.kafka.env")


class Settings(BaseSettings):
    KAFKA_BOOTSTRAP_SERVERS: str
    ORDER_CREATE_TOPIC: str
    ORDER_VALIDATE_TOPIC: str
    ORDER_DELETE_TOPIC: str
    ORDER_CONSUMER_GROUP: str
    loop = asyncio.get_event_loop

    class Config:
        env_file = ".kafka.env"


@lru_cache()
def getSettings():
    return Settings()