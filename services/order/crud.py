from services.order.schemas import OrderIn
from services.order.models import Order
from services.wallet.crud import getCurrencyWallet
from services.wallet.models import Wallet
from services.db.db import db


async def getOrder(orderId: id):
    query = Order.select().where(Order.c.id == orderId)
    return await db.fetch_all(query=query)


async def getOrders():
    query = Order.select()
    return await db.fetch_all(query=query)


async def validateOrder(order: OrderIn, userId: int):
    wallet = await getCurrencyWallet(currencyId=order.currency_id, userId=userId)
    if wallet.quantity < order.quantity:
        return False
    return True


async def createOrder(orderIn: OrderIn):
    query = Order.insert().values(orderIn.dict())
    await db.execute(query=query)


async def updateOrder(orderIn: OrderIn):
    query = Order.update().where(Order.c.id == OrderIn.id).values(orderIn.dict())
    await db.execute(query=query)


async def deleteOrder(orderId: int):
    query = Order.delete().where(Order.c.id == orderId)
    await db.execute(query=query)
