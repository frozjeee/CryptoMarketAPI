from fastapi import FastAPI
from routes import router
from db import database 
import uvicorn

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(router)
 

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8001)