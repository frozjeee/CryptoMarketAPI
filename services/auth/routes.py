from fastapi import APIRouter, status
from schemas import UserIn, UserLogin
from aiokafka import AIOKafkaProducer
from configs.config import (credentialsException,
    userAlreadyExistsException)
from configs.kafkaConfig import (loop,
    KAFKA_BOOTSTRAP_SERVERS, REGISTER_TOPIC)
from schemas import TokenData
import crud


router = APIRouter()


@router.post("/login")
async def login_for_access_token(payload: UserLogin):
    user = await crud.authenticateUser(payload)
    if not user:
        raise credentialsException
    user = TokenData.parse_obj(user)
    accessToken = crud.createAccessToken(user)
    return {
        "status_code": status.HTTP_200_OK,
        "access_token": accessToken, 
        "token_type": "Bearer"}


@router.post("/register")
async def register(payload: UserIn):
    producer = AIOKafkaProducer(
    loop=loop, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()
    try:
        user = await crud.getUser(payload.email)
        if user:
            raise userAlreadyExistsException
        userCredentialsJson = crud.encodeToJson(payload)
        await producer.send_and_wait(topic=REGISTER_TOPIC, value=userCredentialsJson)
        return {
            "status_code": status.HTTP_201_CREATED,
            "detail": "User registered successfully"}
    finally:
        await producer.stop()



