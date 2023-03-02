from fastapi import APIRouter, Depends, HTTPException, status

from services.user.models import User
from services.order import schemas, crud
from services.auth.deps import getCurrentUser


router = APIRouter()


@router.get("/{orderId}/", status_code=status.HTTP_200_OK)
async def getOrder(orderId: int):
    return await crud.getOrder(orderId)


@router.get("/", status_code=status.HTTP_200_OK)
async def getOrders():
    return await crud.getOrders()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def createOrder(orderIn: schemas.OrderIn, user: User = Depends(getCurrentUser)):
    isValid = await crud.validateOrder(orderIn, user.id)
    if not isValid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough money"
        )
    await crud.createOrder(orderIn)


@router.patch("/{orderId}/", status_code=status.HTTP_204_NO_CONTENT)
async def updateOrder(orderIn: schemas.OrderIn, user: User = Depends(getCurrentUser)):
    await crud.updateOrder(orderIn)


@router.delete("/{orderId}/", status_code=status.HTTP_204_NO_CONTENT)
async def deleteOrder(orderId: int, user: User = Depends(getCurrentUser)):
    await crud.deleteOrder(orderId)
