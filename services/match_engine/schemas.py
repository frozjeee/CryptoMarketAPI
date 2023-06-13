from pydantic import BaseModel, Field
from pyllist import sllist

from services.order.schemas import OrderOut


class MatchedOrders(BaseModel):
    buyOrder: OrderOut = Field()
    sellOrder: OrderOut = Field()
    type: str = Field()


class OrderLL(BaseModel):
    buy: sllist = Field()
    sell: sllist = Field()

    class Config:
        arbitrary_types_allowed = True


class MatchedOrdersAndAllOrders(BaseModel):
    matchedOrders: MatchedOrders = Field()
    currenciesOrders: list = Field()
