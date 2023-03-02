from fastapi import APIRouter, Depends, status, Path, HTTPException
from aiokafka import AIOKafkaProducer

from services.user import crud, schemas, models
from services.auth.deps import getCurrentUser
import config.config as settings


router = APIRouter()


@router.get("/{userId}/", response_model=schemas.UserOut, status_code=200)
async def getUser(userId: int = Path(...)):
    return await getUser(userId)


@router.patch("/{userId}/", response_model=schemas.UserOut, status_code=200)
async def updateUser(
    payload: schemas.UserIn,
    userUpdate: schemas.UserIn,
    user: models.User = Depends(getCurrentUser),
):
    updatedUser = await crud.updateUser(userUpdate)

    return updatedUser


@router.delete("/{userId}/", status_code=status.HTTP_204_NO_CONTENT)
async def deleteUser(
    userId: int = Path(...), user: models.User = Depends(getCurrentUser)
):
    if not user.id == userId or not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enought rights"
        )

    await crud.deleteUser(userId=userId)


# @router.post("/{id}/verify")
# async def verifyUser(
#     payload: schemas.UserVerify = Depends(schemas.UserVerify.asForm),
#     user: models.User = Depends(getCurrentUser),
# ):
#     producer = AIOKafkaProducer(
#                 loop=settings.loop(),
#                 bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
#                 max_request_size=10000000,
#                 compression_type="gzip")
#     await producer.start()
#     try:
#         await payload.toBase64()
#         imagesJson = payload.json().encode("utf-8")
#         await producer.send_and_wait(
#                 topic=settings.USER_VERIFY_TOPIC,
#                 value=imagesJson)
#         return {"status_code": status.HTTP_200_OK,
#                 "message": "User verification sent"}
#     finally:
#         await producer.stop()
