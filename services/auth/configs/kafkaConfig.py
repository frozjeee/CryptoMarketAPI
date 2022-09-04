from functools import lru_cache
from pydantic import BaseSettings
from dotenv import load_dotenv
import asyncio


load_dotenv("configs/.kafka.env")


class Settings(BaseSettings):
    KAFKA_BOOTSTRAP_SERVERS: str
    REGISTER_TOPIC: str
    USER_UPDATE_TOPIC: str
    USER_DELETE_TOPIC: str
    KAFKA_CONSUMER_GROUP: str
    loop = asyncio.get_event_loop


    class Config:
        env_file = ".kafka.env"


@lru_cache()
def getSettings():
    return Settings()