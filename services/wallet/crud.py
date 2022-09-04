from datetime import datetime
from aiokafka import AIOKafkaConsumer
from schemas import WalletIn
from db import (Wallet, Currency,
                database as db, 
                currency_database as currency_db)
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


# async def getUserByEmail(email):
#     query = User.select()
#     return await db.fetch_one(query=query, values=email)


# async def deleteOrder(settings: kafkaConfig.Settings = Depends(kafkaConfig.getSettings)):
#     consumer = AIOKafkaConsumer(settings.ORDER_CREATE_TOPIC,
#                                 loop=settings.loop,
#                                 bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
#                                 group_id=settings.ORDER_CONSUMER_GROUP)
#     await consumer.start()
#     try:
#         async for msg in consumer:
#             payload = OrderOut.parse_raw(msg.value)
#             query = User.delete().where(User.c.id==payload.id)
#             await db.execute(query=query)
#     finally:
#         await consumer.stop()




