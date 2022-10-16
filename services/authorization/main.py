from fastapi import FastAPI
from authorization import validateToken
import asyncio


app = FastAPI()

asyncio.create_task(validateToken())
