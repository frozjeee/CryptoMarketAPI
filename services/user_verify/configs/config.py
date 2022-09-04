from functools import lru_cache
from dotenv import load_dotenv
from pydantic import BaseSettings


load_dotenv("configs/.env")


class Settings(BaseSettings):
    ID_ANALYZER_API_KEY: str
    ID_ANALYZER_REGION: str
    DocumentNotAuthentic: Exception = Exception
    FacesNotIdentical: Exception = Exception

    class Config:
        env_file = ".env"


@lru_cache()
def getSettings():
    return Settings()