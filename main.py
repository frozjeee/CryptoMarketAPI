from fastapi import FastAPI
from router import router
from services.db.db import db


app = FastAPI()
app.include_router(router)


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()
