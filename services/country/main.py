from fastapi import FastAPI
from routes import router
from db import database
import asyncio
import crud


app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(router)

asyncio.create_task(crud.createCountry())
asyncio.create_task(crud.updateCountry())
asyncio.create_task(crud.deleteCountry()) 
