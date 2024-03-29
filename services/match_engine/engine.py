from typing import Optional
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from schemas import OrderIn, OrderLL, MatchedOrder
from pyllist import sllist, sllistnode
from db import (
    Currency, Order,
    currency_database as currency_db,
    order_database as order_db
)
import configs.kafkaConfig as kafkaConfig
import json


async def receiveOrder(kafkaSettings: kafkaConfig.Settings = kafkaConfig.getSettings()):
    ordersQuery = Order.select().where(Order.c.status == "pending")
    orders = await order_db.fetch_all(ordersQuery)
    
    currenciesOrders = {}
    currenciesQuery = Currency.select()
    currencies = await currency_db.fetch_all(currenciesQuery)
    for currency in currencies:
        currenciesOrders[currency.get("id")] = OrderLL(buy=sllist(), sell=sllist())
    for order in orders:
       addToOrders(order, currenciesOrders)

    consumer = AIOKafkaConsumer(kafkaSettings.ORDER_MATCH_TOPIC,
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
            addToOrders(order, currenciesOrders)
            while True:
                orderMatch: MatchedOrder = matchOrder(currenciesOrders, order.currency_id)
                if not orderMatch:
                    break
                orderMatch = json.dumps(orderMatch).encode("utf-8")
                producer.send_and_wait(topic=kafkaSettings.ORDER_FULFILL_TOPIC, value=orderMatch)
                if not orderMatch.restart:
                    break
    finally:
        await producer.stop()
        await consumer.stop()


def matchOrder(currenciesOrders, currencyId) -> Optional[MatchedOrder]:
    orderMatch = None
    buyOrder: sllistnode = currenciesOrders[currencyId].buy.first
    sellOrders: sllist = currenciesOrders[currencyId].sell
    buyOrders: sllist = currenciesOrders[currencyId].buy
    for orderIndex, sellOrder in enumerate(sellOrders.iternodes()):
        if sellOrder.value.price <= buyOrder.value.price:

            if buyOrder.value.quantity < sellOrder.value.quantity:
                orderMatch = MatchedOrder(buyOrder.value, sellOrder.value, "buy", False)

                sellOrders.nodeat(orderIndex).value.quantity = \
                                       buyOrder.value.quantity - sellOrder.value.quantity
                buyOrders.popleft()  
                break

            elif buyOrder.value.quantity > sellOrder.value.quantity:
                orderMatch = MatchedOrder(buyOrder.value, sellOrder.value, "sell", True)

                buyOrders.nodeat(0).value.quantity = \
                                    buyOrder.value.quantity - sellOrder.value.quantity
                sellOrders.remove(sellOrder)
                break
            else:
                orderMatch = MatchedOrder(buyOrder.value, sellOrder.value, "both", False)

                buyOrders.popleft()  
                sellOrders.remove(sellOrder)
                break
    if not orderMatch:
        return None
    return orderMatch


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
    