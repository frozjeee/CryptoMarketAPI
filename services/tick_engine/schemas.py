from uuid import UUID
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from pyllist import sllist


class Order(BaseModel):
    id: UUID
    user_id: str
    currency_id: str
    type: str
    price: float
    quantity: float
    status: str
    ordered_at: datetime


class MatchedOrders(BaseModel):
    buyOrder: Order
    sellOrder: Order
    type: str

