from uuid import UUID
from pydantic import BaseModel
from datetime import datetime
from pyllist import sllist


class OrderIn(BaseModel):
    id: UUID
    user_id: str
    currency_id: str
    type: str
    price: float
    quantity: float
    status: str
    ordered_at: datetime


class MatchedOrder(BaseModel):
    buyOrder: OrderIn
    sellOrder: OrderIn
    type: str
    restart: bool


class OrderLL(BaseModel):
    buy: sllist
    sell: sllist

    class Config:
        arbitrary_types_allowed = True


class MatchedOrdersAndAllOrders(BaseModel):
    matchedOrders: MatchedOrder
    currenciesOrders: list