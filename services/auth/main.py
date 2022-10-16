from fastapi import FastAPI
from routes import router
from db import database
import uvicorn


app = FastAPI()

app.include_router(router)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8001)
