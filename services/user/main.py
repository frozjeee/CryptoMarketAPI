from fastapi import FastAPI
from routes import router
from db import database
import asyncio
import uvicorn
import crud


app = FastAPI()

app.include_router(router)

@app.on_event("startup")
async def startup():
    asyncio.create_task(crud.createUser())
    asyncio.create_task(crud.updateUser())
    asyncio.create_task(crud.deleteUser())
    asyncio.create_task(crud.verifiedUser())
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8000)