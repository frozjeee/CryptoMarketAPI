from fastapi import FastAPI
import asyncio
import uvicorn
import crud


app = FastAPI()


@app.on_event("startup")
async def startup():
    asyncio.create_task(crud.verifyUser()) 


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8002)
