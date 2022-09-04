from fastapi import FastAPI
from db import (currency_database,
                order_database)
import asyncio
import uvicorn
import engine


app = FastAPI()


@app.on_event("startup")
async def startup():
    await currency_database.connect()
    asyncio.create_task(engine.receiveOrder()) 


@app.on_event("shutdown")
async def shutdown():
    await currency_database.disconnect()


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8006)