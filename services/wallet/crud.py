from decimal import Decimal

from services.order.schemas import OrderIn
from services.wallet.schemas import WalletIn
from services.wallet.models import Wallet
from services.currency.crud import getCurrencies
from services.db.db import db


async def getWallet(userId: int):
    query = Wallet.select().where(Wallet.c.user_id == userId)
    await db.fetch_all(query=query)


async def getCurrencyWallet(userId: int, currencyId: int):
    query = (
        Wallet.select()
        .where(Wallet.c.userId == userId)
        .where(Wallet.c.currency_id == currencyId)
    )
    return await db.fetch_one(query=query)


async def addMoneyWallet(userId: int, currencyId: int, sum: Decimal):
    query = Wallet.insert().where()


async def createWallet(wallet: WalletIn):
    currencies = await getCurrencies()
    walletQuery = Wallet.insert()
    for currency in currencies:
        await db.execute(
            query=walletQuery,
            values={
                "user_id": wallet.id,
                "currency_id": currency.id,
                "quantity": wallet.quantity,
                "created_at": wallet.created_at,
            },
        )


async def transactOrderMoney(order: OrderIn):
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

        db.execute(walletQuery)
    else:
        pass
