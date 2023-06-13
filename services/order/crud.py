from sqlalchemy import select, update, delete
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from services.order.schemas import OrderIn
from services.order.models import Order
from services.wallet.crud import getCurrencyWallet
from services.user.crud import getUserById


async def getOrder(db: AsyncSession, id: int):
    q = select(Order).filter(Order.id == id)
    cur = await db.execute(q)
    return cur.scalars().one()


async def getOrders(db: AsyncSession, user_id: int):
    q = select(Order).options(joinedload(Order.currency))
    cur = await db.execute(q)
    return cur.scalars().all()


async def validateOrder(db: AsyncSession, order: OrderIn, userId: int):
    if order.type == "buy":
        user = await getUserById(db=db, id=userId)
        if user.balance < order.quantity:
            return False
    else:
        wallet = await getCurrencyWallet(
            db=db, currencyId=order.currency_id, userId=userId
        )
        if wallet.quantity < order.quantity:
            return False
    return True


async def createOrder(db: AsyncSession, orderIn: OrderIn, userId: int):
    order_dict = orderIn.dict()
    order_dict["created_by"] = userId
    order_dict["init_quantity"] = orderIn.quantity
    if orderIn.type == "sell":
        order_dict["seller_id"] = userId
    else:
        order_dict["buyer_id"] = userId
    order = Order(**order_dict)

    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order


async def updateOrder(db: AsyncSession, orderIn: OrderIn):
    q = update(Order). \
        filter(Order.id == orderIn.id). \
        values(orderIn.dict(exclude_none=True))

    await db.execute(q)


async def deleteOrder(db: AsyncSession, orderId: int):
    q = delete(Order).filter(Order.id == orderId)
    await db.execute(q)
