from fastapi import FastAPI, staticfiles
from router import router
from fastapi.middleware.cors import CORSMiddleware

from services.broker.base_class import MessageBroker


app = FastAPI()
app.include_router(router)
app.mount("/static", staticfiles.StaticFiles(directory="static"), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

async def startup():
    broker = MessageBroker()
    app.state.broker = broker

    await broker.startup()


async def shutdown():
    await app.state.broker.shutdown()


app.add_event_handler("startup", startup)
app.add_event_handler("shutdown", shutdown)
    