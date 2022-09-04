from datetime import datetime
import json
from uuid import uuid4
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from fastapi import Depends
from schemas import OrderIn, OrderOut
from db import Order, database as db
import configs.kafkaConfig as kafkaConfig 


async def createOrder(kafkaSettings: kafkaConfig.Settings = kafkaConfig.getSettings()):
    consumer = AIOKafkaConsumer(kafkaSettings.ORDER_CREATE_TOPIC,
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
            order.id = uuid4()
            order.ordered_at = datetime.today().replace(microsecond=0)
            print(order)
            orderJson = order.json().encode("utf-8")
            await producer.send_and_wait(topic=kafkaSettings.ORDER_VALIDATE_TOPIC, value=orderJson)
    finally:
        await producer.stop()
        await consumer.stop()


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