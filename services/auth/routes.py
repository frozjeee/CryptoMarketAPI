from fastapi import APIRouter, status, Depends
from schemas import UserIn, UserLogin
from aiokafka import AIOKafkaProducer
from schemas import TokenData
import configs.kafkaConfig as kafkaConfig
import configs.config as config
import crud


router = APIRouter()


@router.post("/login")
async def login(
        payload: UserLogin,
        settings: config.Settings = Depends(config.getSettings)
):

    user = await crud.authenticateUser(payload)
    if not user:
        raise settings.BaseHTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not exist")

    user = TokenData.parse_obj(user)
    accessToken = crud.createAccessToken(user)

    return {
        "status_code": status.HTTP_200_OK,
        "access_token": accessToken,
        "token_type": "Bearer"}


@router.post("/register")
async def register(
        payload: UserIn,
        settings: config.Settings = Depends(config.getSettings),
        kafkaSettings: kafkaConfig.Settings = Depends(kafkaConfig.getSettings)
):
    producer = AIOKafkaProducer(
        loop=kafkaSettings.loop(),
        bootstrap_servers=kafkaSettings.KAFKA_BOOTSTRAP_SERVERS
    )
    await producer.start()
    try:
        user = await crud.getUser(payload.email)
        if user:
            raise settings.BaseHTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exists")
        userCredentialsJson = payload.json().encode("utf-8")
        await producer.send_and_wait(
                topic=kafkaSettings.REGISTER_TOPIC, value=userCredentialsJson)
        return {
            "status_code": status.HTTP_201_CREATED,
            "detail": "User registered successfully"}
    finally:
        await producer.stop()
