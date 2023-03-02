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

    # Apache Kafka  
    KAFKA_BOOTSTRAP_SERVERS: str
    ORDER_MATCH_TOPIC: str
    ORDER_FULFILL_TOPIC: str
    ORDER_CONSUMER_GROUP: str
    ORDER_MATCH_TOPIC: str
    ORDER_VALIDATE_TOPIC: str
    TRANSACT_ORDER_MONEY: str
    REGISTER_TOPIC: str
    USER_VERIFY_TOPIC: str
    USER_VERIFIED_TOPIC: str
    TRANSACTIONAL_ID: str

    class Config:
        env_file = ".env"


settings = Settings()
