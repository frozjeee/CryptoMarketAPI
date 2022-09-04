from fastapi import FastAPI
from db import wallet_db, order_db
import asyncio
import crud
import uvicorn


app = FastAPI()


@app.on_event("startup")
async def startup():
    asyncio.create_task(crud.validateOrder()) 
    await wallet_db.connect()
    await order_db.connect()


@app.on_event("shutdown")
async def shutdown():
    await wallet_db.disconnect()
    await order_db.disconnect()


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8006)