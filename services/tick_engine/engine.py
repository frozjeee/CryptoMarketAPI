from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from schemas import MatchedOrders
from db import (
    Order,
    Wallet,
    order_database as orderDB,
    wallet_database as walletDB,
    currency_database as currencyDB,
)
import configs.kafkaConfig as kafkaConfig


async def transactionOrders(
    kafkaSettings: kafkaConfig.Settings = kafkaConfig.getSettings(),
):
    consumer = AIOKafkaConsumer(
        kafkaSettings.ORDER_FULFILL_TOPIC,
        loop=kafkaSettings.loop(),
        bootstrap_servers=kafkaSettings.KAFKA_BOOTSTRAP_SERVERS,
        group_id=kafkaSettings.ORDER_CONSUMER_GROUP,
    )

    producer = AIOKafkaProducer(
        loop=kafkaSettings.loop(),
        bootstrap_servers=kafkaSettings.KAFKA_BOOTSTRAP_SERVERS,
    )

    await producer.start()
    await consumer.start()
    try:
        async for msg in consumer:
            print(msg)
            matchedOrders = MatchedOrders.parse_obj(msg)

            userBuyWalletQuery = (
                Wallet.select()
                .where(Wallet.c.user_id == matchedOrders.buyOrder.user_id)
                .where(Wallet.c.currency_id == matchedOrders.buyOrder.currency_id)
            )
            userBuyWallet = await orderDB.fetch_one(query=userBuyWalletQuery)

            userSellWalletQuery = (
                Wallet.select()
                .where(Wallet.c.user_id == matchedOrders.sellOrder.user_id)
                .where(Wallet.c.currency_id == matchedOrders.sellOrder.currency_id)
            )
            userSellWallet = await orderDB.fetch_one(query=userSellWalletQuery)

            orderTrans = await orderDB.transaction()
            walletTrans = await walletDB.transaction()
            currencyTrans = await currencyDB.transaction()
            try:
                if not matchedOrders.type in ["buy, sell"]:
                    sellUpdateOrderQuery = (
                        Order.update()
                        .where(Order.c.id == matchedOrders.buyOrder.id)
                        .values(status="fulfilled")
                    )
                    buyUpdateOrderQuery = (
                        Order.update()
                        .where(Order.c.id == matchedOrders.sellOrder.id)
                        .values(status="fulfilled")
                    )
                    orderDB.execute([buyUpdateOrderQuery, sellUpdateOrderQuery])
                else:
                    if matchedOrders.type == "buy":
                        updateOrderQuery = (
                            Order.update()
                            .where(Order.c.id == matchedOrders.buyOrder.id)
                            .values(status="fulfilled")
                        )
                    else:
                        updateOrderQuery = (
                            Order.update()
                            .where(Order.c.id == matchedOrders.sellOrder.id)
                            .values(status="fulfilled")
                        )
                    orderDB.execute(updateOrderQuery)

                buyQuantityUpdateQuery = (
                    Wallet.update()
                    .where(Wallet.c.user_id == matchedOrders.buyOrder.user_id)
                    .where(Wallet.c.currency_id == matchedOrders.buyOrder.currency_id)
                    .values(
                        quantity=userBuyWallet.quantity
                        - matchedOrders.sellOrder.quantity
                    )
                )

                sellQuantityUpdateQuery = (
                    Wallet.update()
                    .where(Wallet.c.user_id == matchedOrders.sellOrder.user_id)
                    .where(Wallet.c.currency_id == matchedOrders.sellOrder.currency_id)
                    .values(
                        quantity=userSellWallet.quantity
                        + matchedOrders.sellOrder.quantity
                    )
                )

                walletDB.execute(buyQuantityUpdateQuery)
                walletDB.execute(sellQuantityUpdateQuery)
            except:
                await orderTrans.rollback()
                await walletTrans.rollback()
                await currencyTrans.rollback()
            else:
                await orderTrans.commit()
                await walletTrans.commit()
                await currencyTrans.commit()
    finally:
        await producer.stop()
        await consumer.stop()
