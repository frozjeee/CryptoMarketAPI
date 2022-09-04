from fastapi import FastAPI
import uvicorn
from routes import router
import asyncio
import crud
from db import database


app = FastAPI()


@app.on_event("startup")
async def startup():
    asyncio.create_task(crud.createOrder()) 
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8005)