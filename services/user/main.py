import inspect
from fastapi import FastAPI
from routes import router
import asyncio
import crud
from db import database


app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(router)


asyncio.create_task(crud.createUser()) 
asyncio.create_task(crud.updateUser()) 
asyncio.create_task(crud.deleteUser()) 