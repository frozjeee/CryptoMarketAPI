from typing import Optional
from fastapi import APIRouter, Depends, Header, status
from aiokafka import AIOKafkaProducer
from schemas import (UserShow, UserUpdate, 
                    UserOut, UserVerify)
import configs.kafkaConfig as kafkaConfig
import configs.config as config
import authorization


router = APIRouter()


# @router.get("/{email}/", response_model=UserShow)
# async def getUser(email: str):
#     return await getUser(email)
    

@router.patch("/")
async def updateUser(
        payload: UserUpdate,
        Authorization: Optional[str] = Header(None),
        settings: config.Settings = Depends(config.getSettings),
        kafkaSettings: kafkaConfig.Settings = Depends(kafkaConfig.getSettings)):
    tokenData = authorization.validateToken(Authorization)
    if not payload.id == tokenData.id and not tokenData.is_superuser:
        raise settings.BaseHTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough rights",)
    producer = AIOKafkaProducer(
        loop=kafkaSettings.loop(), bootstrap_servers=kafkaSettings.KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()
    try:
        userJson = payload.json().encode("utf-8")
        await producer.send_and_wait(topic=kafkaSettings.USER_UPDATE_TOPIC, value=userJson)
        return {"status_code": status.HTTP_200_OK,
                "message": "User updated successfully"}
    finally:
        await producer.stop()


@router.delete("/")
async def deleteUser(
        payload: UserOut,
        Authorization: Optional[str] = Header(None),
        settings: config.Settings = Depends(config.getSettings),
        kafkaSettings: kafkaConfig.Settings = Depends(kafkaConfig.getSettings)):
    tokenData = authorization.validateToken(Authorization)
    if not payload.id == tokenData.id and not tokenData.is_superuser:
        raise settings.BaseHTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enought rights")
    producer = AIOKafkaProducer(
    loop=kafkaSettings.loop(), bootstrap_servers=kafkaSettings.KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()
    try:
        userIdJson = payload.json().encode("utf-8")
        await producer.send_and_wait(topic=kafkaSettings.USER_DELETE_TOPIC, value=userIdJson)
        return {"status_code": status.HTTP_200_OK,
                "message": "User deleted successfully"}
    finally:
        await producer.stop()


@router.post("/verify")
async def verifyUser(
        payload: UserVerify = Depends(UserVerify.asForm),
        Authorization: Optional[str] = Header(None),
        settings: config.Settings = Depends(config.getSettings),
        kafkaSettings: kafkaConfig.Settings = Depends(kafkaConfig.getSettings)):
    tokenData = authorization.validateToken(Authorization)
    if not tokenData.id:
        raise settings.BaseHTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"})
    producer = AIOKafkaProducer(
                loop=kafkaSettings.loop(), 
                bootstrap_servers=kafkaSettings.KAFKA_BOOTSTRAP_SERVERS,
                max_request_size=10000000,
                compression_type="gzip")
    await producer.start()
    try:
        await payload.toBase64()
        imagesJson = payload.json().encode("utf-8")
        await producer.send_and_wait(
                topic=kafkaSettings.USER_VERIFY_TOPIC, 
                value=imagesJson)
        return {"status_code": status.HTTP_200_OK,
                "message": "User verification sent"}
    finally:
        await producer.stop()