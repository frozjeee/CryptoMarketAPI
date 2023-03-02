from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class Order(BaseModel):
    id: id
    user_id: str
    currency_id: str
    type: str
    price: Decimal
    quantity: Decimal
    status: str
    ordered_at: datetime


class MatchedOrders(BaseModel):
    buyOrder: Order
    sellOrder: Order
    type: str
