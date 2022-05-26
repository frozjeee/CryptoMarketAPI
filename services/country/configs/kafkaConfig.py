import asyncio


KAFKA_BOOTSTRAP_SERVERS = "localhost:9093"
COUNTRY_CREATE_TOPIC = "country-create"
COUNTRY_UPDATE_TOPIC = "country-update"
COUNTRY_DELETE_TOPIC = "country-delete"
COUNTRY_CONSUMER_GROUP = "country"
loop = asyncio.get_event_loop()