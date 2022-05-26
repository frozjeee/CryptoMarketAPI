from typing import Optional
from fastapi import APIRouter, Header, status
from aiokafka import AIOKafkaProducer
from configs.kafkaConfig import (
    loop, KAFKA_BOOTSTRAP_SERVERS, 
    USER_UPDATE_TOPIC, USER_DELETE_TOPIC)
from configs.config import (forbiddenException)
from schemas import UserShow, UserUpdate, UserOut
import authorization
import crud


router = APIRouter()


@router.get("/{email}/", response_model=UserShow)
async def getUser(email: str):
    return await getUser(email)
    

@router.patch("/")
async def updateUser(
        payload: UserUpdate,
        Authorization: Optional[str] = Header(None)):
    tokenData = authorization.validateToken(Authorization)
    if not payload.id == tokenData.id and not tokenData.is_superuser:
        raise forbiddenException
    producer = AIOKafkaProducer(
    loop=loop, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()
    try:
        userJson = crud.encodeToJson(payload)
        await producer.send_and_wait(topic=USER_UPDATE_TOPIC, value=userJson)
        return {"status_code": status.HTTP_200_OK,
                "message": "User updated successfully"}
    finally:
        await producer.stop()


@router.delete("/")
async def deleteUser(
        payload: UserOut,
        Authorization: Optional[str] = Header(None)):
    tokenData = authorization.validateToken(Authorization)
    if not payload.id == tokenData.id and not tokenData.is_superuser:
        raise forbiddenException
    producer = AIOKafkaProducer(
    loop=loop, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()
    try:
        userIdJson = crud.encodeToJson(payload)
        await producer.send_and_wait(topic=USER_DELETE_TOPIC, value=userIdJson)
        return {"status_code": status.HTTP_200_OK,
                "message": "User deleted successfully"}
    finally:
        await producer.stop()

