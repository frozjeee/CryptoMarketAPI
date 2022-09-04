from fastapi import FastAPI
from routes import router
from db import database
import asyncio
import uvicorn
import crud


app = FastAPI()

@app.on_event("startup")
async def startup():
    asyncio.create_task(crud.createCurrency())
    asyncio.create_task(crud.updateCurrency())
    asyncio.create_task(crud.deleteCurrency())
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8004)
