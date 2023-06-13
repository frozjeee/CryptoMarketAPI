from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status, Path, Response, HTTPException

from services.db.deps import get_db_session
from services.user import crud, schemas, models
from services.auth.deps import getCurrentUser
from services.auth.crud import createAccessToken
from services.wallet.crud import createWallet


router = APIRouter()


@router.get("/{pk}/", response_model=schemas.UserOutSchema, status_code=200)
async def getUser(
    db: AsyncSession = Depends(get_db_session),
    pk: int = Path(...)):
    return await crud.getUserById(db, pk)


@router.patch("/")
async def updateUser(
    userUpdate: schemas.UserInSchema,
    user: models.User = Depends(getCurrentUser),
):
    await crud.updateUser(userUpdate)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/")
async def deleteUser(
    user: models.User = Depends(getCurrentUser)
):
    await crud.deleteUser(userId=user.id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/verify/")
async def verifyUser(
    db: AsyncSession = Depends(get_db_session),
    payload: schemas.UserVerify = Depends(schemas.UserVerify.asForm),
    user: models.User = Depends(getCurrentUser),
):
    verified = await crud.verifyUser(payload)
    if verified:
        accessToken = createAccessToken(user)
        await crud.updateUser(db=db, user=schemas.UserUpdateSchema(id=user.id, verified=True))
        await createWallet(db, userId=user.id)
        return {"accessToken": accessToken}
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User was not verified")
