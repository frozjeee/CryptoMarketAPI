from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from schemas import OrderIn
import configs.kafkaConfig as kafkaConfig 



async def validateOrder(kafkaSettings: kafkaConfig.Settings = kafkaConfig.getSettings()):
    consumer = AIOKafkaConsumer(kafkaSettings.ORDER_VALIDATE_TOPIC,
                                loop=kafkaSettings.loop(),
                                bootstrap_servers=kafkaSettings.KAFKA_BOOTSTRAP_SERVERS,
                                group_id=kafkaSettings.ORDER_CONSUMER_GROUP)

    producer = AIOKafkaProducer(loop=kafkaSettings.loop(), 
                                bootstrap_servers=kafkaSettings.KAFKA_BOOTSTRAP_SERVERS,
                                transactional_id=kafkaSettings.TRANSACTIONAL_ID)
    await producer.start()
    await consumer.start()
    try:
        async for msg in consumer:
            order = OrderIn.parse_raw(msg.value)
            orderJson = order.json().encode("utf-8")
            try:
                async with producer.transaction():
                    await producer.send_and_wait(topic=kafkaSettings.TRANSACT_ORDER_MONEY, value=orderJson)
                    await producer.send_and_wait(topic=kafkaSettings.ORDER_MATCH_TOPIC, value=orderJson)
            finally:
                await producer.stop()
    finally:
        await consumer.stop()
