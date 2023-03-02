import json

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from schemas import OrderIn, OrderLL, MatchedOrders
from pyllist import sllist, sllistnode

from services.db.db import db
from services.order.models import Order
from services.currency.models import Currency
import config.config as settings


async def receiveOrder():
    ordersQuery = Order.select().where(Order.c.status == "pending")
    orders = await db.fetch_all(ordersQuery)

    currenciesOrders = {}
    currenciesQuery = Currency.select()
    currencies = await db.fetch_all(currenciesQuery)
    for currency in currencies:
        currenciesOrders[currency.get("id")] = OrderLL(buy=sllist(), sell=sllist())
    for order in orders:
        addToOrders(order, currenciesOrders)

    consumer = AIOKafkaConsumer(
        settings.ORDER_MATCH_TOPIC,
        loop=settings.loop(),
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        group_id=settings.ORDER_CONSUMER_GROUP,
    )

    producer = AIOKafkaProducer(
        loop=settings.loop(), bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS
    )

    await producer.start()
    await consumer.start()
    try:
        async for msg in consumer:
            order = OrderIn.parse_raw(msg.value)
            addToOrders(order, currenciesOrders)
            while True:
                matchedOrders = matchOrders(currenciesOrders, order.currency_id)
                if not matchedOrders:
                    break
                matchedOrders = json.dumps(matchedOrders).encode("utf-8")
                producer.send_and_wait(
                    topic=settings.ORDER_FULFILL_TOPIC, value=matchedOrders
                )
                if not matchedOrders.restart:
                    break
    finally:
        await producer.stop()
        await consumer.stop()


def matchOrders(currenciesOrders, currencyId):
    orderMatches = None
    buyOrder: sllistnode = currenciesOrders[currencyId].buy.first
    sellOrders: sllist = currenciesOrders[currencyId].sell
    buyOrders: sllist = currenciesOrders[currencyId].buy
    for orderIndex, sellOrder in enumerate(sellOrders.iternodes()):
        if sellOrder.value.price <= buyOrder.value.price:
            if buyOrder.value.quantity < sellOrder.value.quantity:
                orderMatches = MatchedOrders(
                    buyOrder.value, sellOrder.value, "buy", False
                )
                sellOrders.nodeat(orderIndex).value.quantity = (
                    buyOrder.value.quantity - sellOrder.value.quantity
                )
                buyOrders.popleft()
                break
            elif buyOrder.value.quantity > sellOrder.value.quantity:
                orderMatches = MatchedOrders(
                    buyOrder.value, sellOrder.value, "sell", True
                )
                buyOrders.nodeat(0).value.quantity = (
                    buyOrder.value.quantity - sellOrder.value.quantity
                )
                sellOrders.remove(sellOrder)
                break
            else:
                orderMatches = MatchedOrders(
                    buyOrder.value, sellOrder.value, "both", False
                )
                buyOrders.popleft()
                sellOrders.remove(sellOrder)
                break
    if not orderMatches:
        return None
    return orderMatches


def addToOrders(order, currenciesOrders):
    inserted = False
    if order.type == "buy":
        buyOrders = currenciesOrders[order.get("currency_id")].buy
        for buyOrder in buyOrders.iternodes():
            if buyOrder.value.price < order.price:
                buyOrders.insertbefore(buyOrder, order)
                inserted = True
                break
            elif buyOrder.value.price == order.price:
                buyOrders.insertafter(buyOrder, order)
                inserted = True
                break
        if not inserted:
            buyOrders.appendright(order)
    else:
        sellOrders = currenciesOrders[order.get("currency_id")].sell
        for sellOrder in sellOrders.iternodes():
            if sellOrder.value.price < order.price:
                sellOrders.insertbefore(buyOrder, order)
                inserted = True
                break
            elif sellOrder.value.price == order.price:
                sellOrders.insertafter(buyOrder, order)
                inserted = True
                break
        if not inserted:
            sellOrders.appendright(order)
