from decimal import Decimal

from sqlalchemy import select, update, insert
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from services.order.schemas import OrderIn
from services.wallet.schemas import WalletUpdate
from services.wallet.models import Wallet
from services.currency.crud import getCurrencies
from services.user.crud import getUserById
from services.user.models import User


async def getWallet(db: AsyncSession, userId: int):
    q = select(Wallet).filter(Wallet.user_id == userId).options(joinedload(Wallet.currency))
    cur = await db.execute(q)
    return cur.scalars().all()



async def getCurrencyWallet(db: AsyncSession, currencyId: int, userId: int):
    q = select(Wallet). \
        filter(Wallet.user_id == userId,
               Wallet.currency_id == currencyId)
    cur = await db.execute(q)
    return cur.scalar_one_or_none()


async def takeMoneyWallet(db: AsyncSession, currencyId: int, userId: int, quantity: Decimal):
    wallet = await getCurrencyWallet(db=db, userId=userId, currencyId=currencyId)
    walletChange = update(Wallet). \
        filter(Wallet.user_id == userId, Wallet.currency_id == currencyId). \
        values(quantity=wallet.quantity - quantity)
    await db.execute(walletChange)
    await db.commit()


async def takeMoneyBalance(db: AsyncSession, currencyId: int, userId: int, quantity: Decimal):
    user = await getUserById(db=db, id=userId)
    userBalanceChange = update(User). \
        filter(User.id == userId). \
        values(balance=user.balance - quantity)
    await db.execute(userBalanceChange)
    await db.commit()


async def topUpWallet(db: AsyncSession, walletTopUp: WalletUpdate):
    q = update(Wallet).\
        filter(Wallet.user_id == walletTopUp.user_id,
               Wallet.currency_id == walletTopUp.currency_id). \
        values(quantity=walletTopUp.quantity)
    
    await db.execute(q)
    await db.commit()

async def createWallet(db: AsyncSession, userId: int):
    currencies = await getCurrencies(db)
    await db.execute(
        insert(Wallet),
        [
            dict(
                user_id=userId,
                currency_id=currency.id
            )
            for currency in currencies
        ],
    )

    await db.commit()


async def transactOrderMoney(db: AsyncSession, order: OrderIn):
    userMainBalanceQuery = (
        Wallet.select()
        .where(Wallet.c.user_id == order.user_id)
        .where(Wallet.c.currency_id == order.main_currency)
    )
    userBalanceQuery = (
        Wallet.select()
        .where(Wallet.c.user_id == order.user_id)
        .where(Wallet.c.currency_id == order.currency)
    )

    userMainBalance = await db.fetch_one(userMainBalanceQuery)
    userBalance = await db.fetch_one(userBalanceQuery)

    if (order.quantity * order.price > userMainBalance.quantity) and (
        order.quantity > userBalance.quantity
    ):

        if order.type == "buy":
            walletQuery = (
                Wallet.update()
                .where(Wallet.c.id == order.user_id)
                .where(Wallet.c.currency_id == order.currency_id)
                .values(
                    amount=userMainBalance.quantity - (order.quantity * order.price)
                )
            )
        elif order.type == "sell":
            walletQuery = (
                Wallet.update()
                .where(Wallet.c.id == order.user_id)
                .where(Wallet.c.currency_id == order.currency_id)
                .values(amount=userBalance.quantity - order.quantity)
            )

        await db.execute(walletQuery)
        await db.commit()
    else:
        pass
