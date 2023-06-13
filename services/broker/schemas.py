from decimal import Decimal
from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class OrderMQSchema(BaseModel):
    id: int
    buyer_id: Optional[int]
    seller_id: Optional[int]
    currency_id: int
    type: str
    price: Decimal
    quantity: Decimal
    ordered_at: Optional[datetime]

    class Config: 
        orm_mode = True
