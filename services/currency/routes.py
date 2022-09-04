from typing import Optional
from fastapi import APIRouter, Depends, Header, status
from aiokafka import AIOKafkaProducer
from schemas import CurrencyIn, CurrencyOut, CurrencyUpdate
import configs.kafkaConfig as kafkaConfig
import configs.config as config
import authorization
import crud


router = APIRouter()


@router.get("/{currencyName}")
async def getCurrency(currencyName: str):
    return await crud.getCurrency(currencyName)


@router.post("/")
async def createCurrency(
        payload: CurrencyIn, 
        settings: config.Settings = Depends(config.getSettings),
        kafkaSettings: kafkaConfig.Settings = Depends(kafkaConfig.getSettings),
        Authorization: Optional[str] = Header(None)):
    tokenData = authorization.validateToken(Authorization)
    if not tokenData.is_superuser:
        raise settings.BaseHTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough rights"
        )
    producer = AIOKafkaProducer(
                loop=kafkaSettings.loop(), 
                bootstrap_servers=kafkaSettings.KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()
    try:
        currencyJson = payload.json().encode("utf-8")
        await producer.send_and_wait(
                topic=kafkaSettings.CURRENCY_CREATE_TOPIC, 
                value=currencyJson)
    finally:
        await producer.stop()


@router.patch("/")
async def updateCurrency(
        payload: CurrencyUpdate,
        settings: config.Settings = Depends(config.getSettings),
        kafkaSettings: kafkaConfig.Settings = Depends(kafkaConfig.getSettings),
        Authorization: Optional[str] = Header(None)):
    tokenData = authorization.validateToken(Authorization)
    if not tokenData.is_superuser:
        raise settings.BaseHTTPException(
            status=status.HTTP_403_FORBIDDEN,
            detail="Not enough rights"
        )
    producer = AIOKafkaProducer(
                loop=kafkaSettings.loop(), 
                bootstrap_servers=kafkaSettings.KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()
    try:
        currencyJson = payload.json().encode("utf-8")
        await producer.send_and_wait(
                topic=kafkaSettings.CURRENCY_UPDATE_TOPIC, 
                value=currencyJson)
    finally:
        await producer.stop()


@router.delete("/")
async def deleteCurrency(
        payload: CurrencyOut,
        settings: config.Settings = Depends(config.getSettings),
        kafkaSettings: kafkaConfig.Settings = Depends(kafkaConfig.getSettings),
        Authorization: Optional[str] = Header(None)):
    tokenData = authorization.validateToken(Authorization)
    if not tokenData.is_superuser:
        raise settings.BaseHTTPException(
            status=status.HTTP_403_FORBIDDEN,
            detail="Not enough rights"
        )
    producer = AIOKafkaProducer(
                loop=kafkaSettings.loop(), 
                bootstrap_servers=kafkaSettings.KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()
    try:
        currencyJson = payload.json().encode("utf-8")
        await producer.send_and_wait(
                topic=kafkaSettings.CURRENCY_DELETE_TOPIC, 
                value=currencyJson)
    finally:
        await producer.stop()



