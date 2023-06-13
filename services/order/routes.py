from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from services.broker.publish import publish_message
from services.broker.schemas import OrderMQSchema
from services.broker.deps import get_broker
from services.db.deps import get_db_session
from services.user.models import User
from services.wallet.crud import takeMoneyWallet, takeMoneyBalance
from services.order import schemas, crud
from services.auth.deps import getCurrentUser


router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
async def getOrders(
    user: User = Depends(getCurrentUser),
    db: AsyncSession = Depends(get_db_session)
):
    return await crud.getOrders(db=db, user_id=user.id)


@router.post("/", response_model=schemas.OrderOut, status_code=status.HTTP_201_CREATED)
async def createOrder(
    request: Request,
    orderIn: schemas.OrderIn,
    user: User = Depends(getCurrentUser),
    db: AsyncSession = Depends(get_db_session)
):
    isValid = await crud.validateOrder(db, orderIn, user.id)
    if not isValid:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Not enough money on wallet or balance"
        )
    order = await crud.createOrder(db=db, orderIn=orderIn, userId=user.id)
    if orderIn.type == "buy":
        await takeMoneyBalance(db=db, currencyId=order.currency_id, userId=user.id, quantity=order.init_quantity)
    else:
        await takeMoneyWallet(db=db, currencyId=order.currency_id, userId=user.id, quantity=order.init_quantity)
    order_msg = OrderMQSchema.from_orm(order)
    if orderIn.type == "buy":
        order_msg.buyer_id = user.id
    else:
        order_msg.seller_id = user.id
    await publish_message(get_broker(request), order_msg)
    return order


@router.patch("/{pk}/", status_code=status.HTTP_204_NO_CONTENT)
async def updateOrder(orderIn: schemas.OrderIn, user: User = Depends(getCurrentUser)):
    await crud.updateOrder(orderIn)


@router.delete("/{pk}/", status_code=status.HTTP_204_NO_CONTENT)
async def deleteOrder(pk: int, user: User = Depends(getCurrentUser)):
    await crud.deleteOrder(pk)
