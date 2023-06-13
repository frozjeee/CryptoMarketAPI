from sqlalchemy import (
    DateTime,
    Column,
    ForeignKey,
    Integer,
    String,
    DECIMAL,
)

from services.db.db import Model
from services.common import timezone


class Currency(Model):
    __tablename__ = "currency"

    id = Column(Integer, primary_key=True, unique=True)
    code = Column(String(10))
    name = Column(String(50))
    price = Column(DECIMAL)
    quantity = Column(DECIMAL)
    created_at = Column(DateTime, default=timezone.now)
    updated_at = Column(DateTime, default=timezone.now, onupdate=timezone.now)

    @property
    def market_cap(self):
        return self.price * self.quantity


class CurrencyHistory(Model):
    __tablename__ = "currency_history"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    currency_id = Column(Integer, ForeignKey("currency.id"))
    price = Column(DECIMAL)
    created_at = Column(DateTime, default=timezone.now)
