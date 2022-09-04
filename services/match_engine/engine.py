from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from schemas import OrderIn, OrderLL, MatchedOrders
from pyllist import sllist, sllistnode
from db import (Currency, Order,
                currency_database as currency_db,
                order_database as order_db)
import configs.kafkaConfig as kafkaConfig
import json


async def receiveOrder(kafkaSettings: kafkaConfig.Settings = kafkaConfig.getSettings()):
    ordersQuery = Order.select().where(Order.c.type=="pending")
    orders = await order_db.fetch_all(ordersQuery)
    currenciesOrders = {}
    currenciesQuery = Currency.select()
    currencies = await currency_db.fetch_all(currenciesQuery)
    for currency in currencies:
        currenciesOrders[str(currency.get("id"))] = OrderLL(buy=sllist(), sell=sllist())

    for order in orders:
        if order.type == "buy":
            for buyOrder in currenciesOrders[str(order.get("id"))].buy.iternodes():
                if buyOrder.value.price < order.price:
                    buyOrders.insertbefore(buyOrder, order)
                    break
                elif buyOrder.value.price == order.price:
                    buyOrders.insertafter(buyOrder, order)
                    break
            currenciesOrders[str(order.get("id"))].buy.append
        else:
            currenciesOrders[str(order.get("id"))].sell.append

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
            inserted = False
            if order.type == "buy":
                print(currenciesOrders)
                buyOrders: sllist = currenciesOrders[order.currency_id].buy
                for buyOrder in buyOrders.iternodes():
                    if buyOrder.value.price < order.price:
                        inserted = True
                        buyOrders.insertbefore(buyOrder, order)
                        break
                    elif buyOrder.value.price == order.price:
                        inserted = True
                        buyOrders.insertafter(buyOrder, order)
                        break
                if not inserted:
                    buyOrders.appendright(order)
            else:
                sellOrders: sllist = currenciesOrders[order.currency_id].sell
                for sellOrder in sellOrders.iternodes():
                    if sellOrder.value.price > order.price:
                        inserted = True
                        sellOrders.insertbefore(sellOrder, order)
                        break
                    elif sellOrder.value.price == order.price:
                        inserted = True
                        sellOrders.insertafter(sellOrder, order)
                        break
                if not inserted:
                    sellOrders.appendright(order)
            while True: 
                matchedOrders = matchOrders(currenciesOrders, order.currency_id)
                if not matchedOrders:
                    break
                matchedOrders = json.dumps(matchedOrders).encode("utf-8")
                producer.send_and_wait(topic=kafkaSettings.ORDER_FULFILL_TOPIC, value=matchedOrders)
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
                orderMatches = MatchedOrders(buyOrder.value, sellOrder.value, "buy", False)
                sellOrders.nodeat(orderIndex).value.quantity = \
                                    buyOrder.value.quantity - sellOrder.value.quantity
                buyOrders.popleft()  
                break
            elif buyOrder.value.quantity > sellOrder.value.quantity:
                orderMatches = MatchedOrders(buyOrder.value, sellOrder.value, "sell", True)
                buyOrders.nodeat(0).value.quantity = \
                                    buyOrder.value.quantity - sellOrder.value.quantity
                sellOrders.remove(sellOrder)
                break
            else:
                orderMatches = MatchedOrders(buyOrder.value, sellOrder.value, "both", False)
                buyOrders.popleft()  
                sellOrders.remove(sellOrder)
                break
    if not orderMatches:
        return None
    return orderMatches
 