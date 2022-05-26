import asyncio


KAFKA_BOOTSTRAP_SERVERS = "localhost:9093"
REGISTER_TOPIC = "user-register"
USER_UPDATE_TOPIC = "user-update"
USER_DELETE_TOPIC = "user-delete"
KAFKA_CONSUMER_GROUP = "user"
loop = asyncio.get_event_loop()