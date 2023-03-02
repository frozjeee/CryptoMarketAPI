from sqlalchemy import Column, Table, DECIMAL, DateTime, ForeignKey, Integer, Enum

from services.order import OrderStatusEnum, OrderTypeEnum
from services.db.db import metadata
from services.common import timezone


Order = Table(
    "order",
    metadata,
    Column("id", Integer, primary_key=True, unique=True, autoincrement=True),
    Column("user_id", Integer, ForeignKey("user.id")),
    Column("currency_id", Integer, ForeignKey("currency.id")),
    Column("type", Enum(OrderTypeEnum)),
    Column("price", DECIMAL),
    Column("quantity", DECIMAL),
    Column("status", Enum(OrderStatusEnum)),
    Column("created_at", DateTime, default=timezone.now)
)
