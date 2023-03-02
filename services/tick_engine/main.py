from fastapi import FastAPI
from db import currency_database, order_database, wallet_database
import asyncio
import uvicorn
import engine


app = FastAPI()


@app.on_event("startup")
async def startup():
    asyncio.create_task(engine.transactionOrders())
    await wallet_database.connect()
    await order_database.connect()
    await currency_database.connect()


@app.on_event("shutdown")
async def shutdown():
    await wallet_database.disconnect()
    await order_database.disconnect()
    await currency_database.disconnect()


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8006)
