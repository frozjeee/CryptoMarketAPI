import logging

from sqlalchemy import select, desc, asc, update, insert
from sqlalchemy.ext.asyncio import AsyncSession

from services.broker.schemas import OrderMQSchema
from services.order.models import Order
from services.wallet.models import Wallet
from services.order import OrderTypeEnum, OrderStatusEnum
from services.currency.models import Currency, CurrencyHistory


logger = logging.getLogger("match_engine")
handler = logging.StreamHandler()
formatter = logging.Formatter("[%(levelname)s - %(asctime)s]: %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


async def receiveOrder(db: AsyncSession, order: OrderMQSchema):
    order_q = select(Order).filter(Order.id == order.id)
    cur = await db.execute(order_q)
    db_order_raw = cur.scalar_one_or_none()
    db_order = OrderMQSchema.from_orm(db_order_raw)

    orders_q = select(Order).filter(
            Order.currency_id == db_order.currency_id,
            Order.status == OrderStatusEnum.pending.value)
    if order.type == OrderTypeEnum.buy.value:
        orders_q = orders_q.filter(Order.type == OrderTypeEnum.sell.value). \
            order_by(asc(Order.price))
    else:
        orders_q = orders_q.filter(Order.type == OrderTypeEnum.buy.value). \
            order_by(desc(Order.price))
        
    curr_q = select(Currency).filter(Currency.id == order.currency_id)
    orders_cur = await db.execute(orders_q)
    curr_cur = await db.execute(curr_q)

    orders = orders_cur.scalars().all()
    currency = curr_cur.scalar_one_or_none()

    for ord in orders:
        ord: Order
        fin_price = ord.price - db_order.price
        fin_quantity = ord.quantity - db_order.quantity
        if fin_price >= 0:
            if fin_quantity > 0:
                print("fin_quantity > 0")
                print(ord)
                order_done_q = update(Order).filter(Order.id == db_order.id).values(status=OrderStatusEnum.done.value)
                ord_order_q = update(Order).filter(Order.id == ord.id).values(quantity=fin_quantity)
                await db.execute(order_done_q)
                await db.execute(ord_order_q)
                await transactionOrders(db, ord, db_order)
                break
            elif fin_quantity == 0:
                print("fin_quantity == 0")
                print(ord)
                order_done_q = update(Order).where(Order.id == db_order.id).values(status=OrderStatusEnum.done.value)
                ord_done_q = update(Order).where(Order.id == ord.id).values(status=OrderStatusEnum.done.value)
                await db.execute(order_done_q)
                await db.execute(ord_done_q)

                order_quant_q = update(Order).where(Order.id == db_order.id).values(quantity=0)
                ord_quant_q = update(Order).where(Order.id == ord.id).values(quantity=0)

                await db.execute(order_quant_q)
                await db.execute(ord_quant_q)
                await transactionOrders(db, ord, db_order)
                break
            else:
                print("fin_quantity < 0")
                print(ord)
                order_q = update(Order).filter(Order.id == db_order.id).values(quantity=abs(fin_quantity))
                ord_order_q = update(Order).filter(Order.id == ord.id).values(status=OrderStatusEnum.done.value)
                await db.execute(order_done_q)
                await db.execute(ord_order_q)
                await transactionOrders(db, ord, db_order)
                db_order.quantity = abs(fin_quantity)

    return True


async def transactionOrders(db: AsyncSession, matched_order: Order, order: OrderMQSchema):
    if order.type == OrderTypeEnum.buy.value:
        userBuyWalletQuery = select(Wallet). \
                            filter(Wallet.user_id == order.buyer_id). \
                            filter(Wallet.currency_id == order.currency_id)
        cur = await db.execute(userBuyWalletQuery)
        userBuyWallet = cur.scalar_one_or_none()

        userSellWalletQuery = select(Wallet). \
                            filter(Wallet.user_id == matched_order.seller_id). \
                            filter(Wallet.currency_id == matched_order.currency_id)
        cur = await db.execute(userSellWalletQuery)
        userSellWallet = cur.scalar_one_or_none()
        
        userBuyUpdateWalletQuery = update(Wallet). \
            filter(Wallet.user_id == order.seller_id, Wallet.currency_id == matched_order.currency_id). \
            values(quantity=userBuyWallet.quantity + matched_order.quantity)

        userSellUpdateWalletQuery = update(Wallet). \
            filter(Wallet.user_id == matched_order.seller_id, Wallet.currency_id == matched_order.currency_id). \
            values(quantity=userSellWallet.quantity - matched_order.quantity)

        await db.execute(userBuyUpdateWalletQuery)
        await db.execute(userSellUpdateWalletQuery)
    else:
        userBuyWalletQuery = select(Wallet). \
                            filter(Wallet.user_id == matched_order.buyer_id). \
                            filter(Wallet.currency_id == matched_order.currency_id)
        cur = await db.execute(userBuyWalletQuery)
        userBuyWallet = cur.scalar_one_or_none()

        userSellWalletQuery = select(Wallet). \
                            filter(Wallet.user_id == order.seller_id). \
                            filter(Wallet.currency_id == order.currency_id)
        cur = await db.execute(userSellWalletQuery)
        userSellWallet = cur.scalar_one_or_none()
        
        userBuyUpdateWalletQuery = update(Wallet). \
            filter(Wallet.user_id == matched_order.currency_id, Wallet.currency_id == matched_order.buyer_id). \
            values(quantity=userBuyWallet.quantity + matched_order.quantity)

        userSellUpdateWalletQuery = update(Wallet). \
            filter(Wallet.user_id == order.currency_id, Wallet.currency_id == order.seller_id). \
            values(quantity=userSellWallet.quantity - order.quantity)

        await db.execute(userSellUpdateWalletQuery)
        await db.execute(userBuyUpdateWalletQuery)

    updateCurrPriceQuery = update(Currency). \
            filter(Currency.id == order.currency_i). \
            values(price=order.price)

    updateCurrHistPriceQuery = insert(CurrencyHistory). \
            values(currency_id=order.currency_id, quantity=userSellWallet.quantity - order.quantity)

    await db.execute(updateCurrPriceQuery)
    await db.execute(updateCurrHistPriceQuery)

    await db.commit()
