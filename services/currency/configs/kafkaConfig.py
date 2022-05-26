import asyncio


KAFKA_BOOTSTRAP_SERVERS = "localhost:9093"
CURRENCY_CREATE_TOPIC = "currency-create"
CURRENCY_UPDATE_TOPIC = "currency-update"
CURRENCY_DELETE_TOPIC = "currency-delete"
CURRENCY_CONSUMER_GROUP = "currency"
loop = asyncio.get_event_loop()