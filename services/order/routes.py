from functools import lru_cache
from typing import Optional
from fastapi import APIRouter, Depends, Header, status
from aiokafka import AIOKafkaProducer
from schemas import OrderIn
import configs.kafkaConfig as kafkaConfig 
import configs.config as config 
import authorization
import crud


router = APIRouter()

@lru_cache()
def get_settings():
    return config.Settings()


@router.get("/{order}/")
async def getUser(email: str):
    return await getUser(email)
    


@router.post("/")
async def createOrder(
        payload: OrderIn,
        Authorization: Optional[str] = Header(None),
        settings: config.Settings = Depends(config.getSettings),
        kafkaSettings: kafkaConfig.Settings = Depends(kafkaConfig.getSettings)):
    tokenData = authorization.validateToken(Authorization)
    producer = AIOKafkaProducer(
    loop=kafkaSettings.loop(), bootstrap_servers=kafkaSettings.KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()
    try:
        orderJson = payload.json().encode("utf-8")
        await producer.send_and_wait(topic=kafkaSettings.ORDER_CREATE_TOPIC, value=orderJson)
        return {"status_code": status.HTTP_200_OK,
                "message": "Order request sent"}
    finally:
        await producer.stop()


# @router.patch("/")
# async def updateUser(
#         payload: UserUpdate,
#         Authorization: Optional[str] = Header(None)):
#     tokenData = authorization.validateToken(Authorization)
#     if not payload.id == tokenData.id and not tokenData.is_superuser:
#         raise forbiddenException
#     producer = AIOKafkaProducer(
#     loop=loop, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
#     await producer.start()
#     try:
#         userJson = crud.encodeToJson(payload)
#         await producer.send_and_wait(topic=USER_UPDATE_TOPIC, value=userJson)
#         return {"status_code": status.HTTP_200_OK,
#                 "message": "User updated successfully"}
#     finally:
#         await producer.stop()


# @router.delete("/")
# async def deleteUser(
#         payload: UserOut,
#         Authorization: Optional[str] = Header(None)):
#     tokenData = authorization.validateToken(Authorization)
#     if not payload.id == tokenData.id and not tokenData.is_superuser:
#         raise forbiddenException
#     producer = AIOKafkaProducer(
#     loop=loop, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
#     await producer.start()
#     try:
#         userIdJson = crud.encodeToJson(payload)
#         await producer.send_and_wait(topic=USER_DELETE_TOPIC, value=userIdJson)
#         return {"status_code": status.HTTP_200_OK,
#                 "message": "User deleted successfully"}
#     finally:
#         await producer.stop()

