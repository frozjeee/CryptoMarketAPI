from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from schemas import OrderIn, OrderOut
from db import Wallet, wallet_db, Order, order_db
import configs.kafkaConfig as kafkaConfig 



async def validateOrder(kafkaSettings: kafkaConfig.Settings = kafkaConfig.getSettings()):
    consumer = AIOKafkaConsumer(kafkaSettings.ORDER_VALIDATE_TOPIC,
                                loop=kafkaSettings.loop(),
                                bootstrap_servers=kafkaSettings.KAFKA_BOOTSTRAP_SERVERS,
                                group_id=kafkaSettings.ORDER_CONSUMER_GROUP)

    producer = AIOKafkaProducer(loop=kafkaSettings.loop(), 
                                bootstrap_servers=kafkaSettings.KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()
    await consumer.start()
    try:
        async for msg in consumer:
            order = OrderIn.parse_raw(msg.value)
            userBalanceQuery = Wallet.select().where(Wallet.c.user_id==order.user_id) \
                                            .where(Wallet.c.currency_id==order.currency_id)
            userBalance = await wallet_db.fetch_one(userBalanceQuery)
            if order.quantity > userBalance.quantity:
                pass
            else:
                orderQuery = Order.insert().values(dict(order))
                await order_db.execute(orderQuery)
                orderJson = order.json().encode("utf-8")
                await producer.send_and_wait(topic=kafkaSettings.ORDER_MATCH_TOPIC, value=orderJson)
    finally:
        await consumer.stop()
