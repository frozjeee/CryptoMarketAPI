from datetime import datetime
from aiokafka import AIOKafkaConsumer
from schemas import WalletIn
from db import (
    Wallet,
    Currency,
    MainWallet,
    database as db,
    currency_database as currency_db
)
import configs.kafkaConfig as kafkaConfig 


async def getWallet(wallet: str):
    query = Wallet.select().where(Wallet.id == wallet)
    await db.fetch_all(query=query)


async def createWallet(settings: kafkaConfig.Settings = kafkaConfig.getSettings()):
    consumer = AIOKafkaConsumer(settings.USER_VERIFIED_TOPIC,
                                loop=settings.loop(),
                                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                                group_id=settings.WALLET_CONSUMER_GROUP)
    await consumer.start()
    try:
        async for msg in consumer:
            wallet = WalletIn.parse_raw(msg.value)
            wallet.created_at = datetime.today().replace(microsecond=0)
            currenciesQuery = Currency.select()
            currencies = await currency_db.fetch_all(query=currenciesQuery)
            walletQuery = Wallet.insert()
            for currency in currencies:
                await db.execute(query=walletQuery, values={"user_id": wallet.id, 
                                                            "currency_id": currency.id, 
                                                            "quantity": wallet.quantity, 
                                                            "created_at": wallet.created_at})
    finally:
        await consumer.stop()


async def createMainWallet(settings: kafkaConfig.Settings = kafkaConfig.getSettings()):
    consumer = AIOKafkaConsumer(settings.USER_VERIFIED_TOPIC,
                                loop=settings.loop(),
                                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                                group_id=settings.WALLET_CONSUMER_GROUP)
    await consumer.start()
    try:
        async for msg in consumer:
            wallet = WalletIn.parse_raw(msg.value)
            wallet.created_at = datetime.today().replace(microsecond=0)
            currenciesQuery = Currency.select()
            currencies = await currency_db.fetch_all(query=currenciesQuery)
            walletQuery = Wallet.insert()
            for currency in currencies:
                await db.execute(query=walletQuery, values={"user_id": wallet.id, 
                                                            "currency_id": currency.id, 
                                                            "quantity": wallet.quantity, 
                                                            "created_at": wallet.created_at})
    finally:
        await consumer.stop()


async def getOrderMoney():
    userBalanceQuery = MainWallet.select() \
                                        .where(MainWallet.c.user_id == order.user_id) \
                                        .where(MainWallet.c.currency_id == User)

    userBalance = await wallet_db.fetch_one(userBalanceQuery)
    if order.quantity * order.price > userBalance.quantity:
        pass
    else:
        if order.type == "buy":
            walletQuery = Wallet.update() \
                .where(Wallet.c.id == order.user_id) \
                .where(Wallet.c.currency_id == order.currency_id) \
                .values(amount=userBalance.quantity - (order.quantity * order.price))
        elif order.type == "sell":
            walletQuery = Wallet.update() \
                .where(Wallet.c.id == order.user_id) \
                .where(Wallet.c.currency_id == order.currency_id) \
                .values(amount=userBalance.quantity - order.quantity)
                        