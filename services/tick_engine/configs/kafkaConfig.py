from functools import lru_cache
from dotenv import load_dotenv
from pydantic import BaseSettings
import asyncio


load_dotenv("configs/.kafka.env")


class Settings(BaseSettings):
    KAFKA_BOOTSTRAP_SERVERS: str
    ORDER_DELETE_TOPIC: str
    ORDER_FULFILL_TOPIC: str
    ORDER_UPLOAD_TOPIC: str
    ORDER_CONSUMER_GROUP: str
    loop = asyncio.get_event_loop

    
    class Config:
        env_file = "/.kafka.env"


@lru_cache()
def getSettings():
    return Settings()