from pydantic import BaseModel, Field
from pyllist import sllist

from services.order.schemas import OrderIn


class MatchedOrders(BaseModel):
    buyOrder: OrderIn = Field()
    sellOrder: OrderIn = Field()
    type: str = Field()
    restart: bool = Field()


class OrderLL(BaseModel):
    buy: sllist = Field()
    sell: sllist = Field()

    class Config:
        arbitrary_types_allowed = True


class MatchedOrdersAndAllOrders(BaseModel):
    matchedOrders: MatchedOrders = Field()
    currenciesOrders: list = Field()
