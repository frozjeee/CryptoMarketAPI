from fastapi import FastAPI
import uvicorn
from routes import router
import asyncio
import crud
from db import database, currency_database


app = FastAPI()


@app.on_event("startup")
async def startup():
    asyncio.create_task(crud.createWallet()) 
    await database.connect()
    await currency_database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    await currency_database.disconnect()


app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8003)

