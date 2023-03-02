from sqlalchemy import (
    DateTime,
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
    DECIMAL,
)

from services.db.db import metadata
from services.common import timezone


Currency = Table(
    "currency",
    metadata,
    Column("id", Integer, primary_key=True, unique=True),
    Column("code", String(10)),
    Column("name", String(50)),
    Column("price", DECIMAL),
    Column("quantity", DECIMAL),
    Column("market_cap", DECIMAL),
    Column("created_at", DateTime, default=timezone.now),
    Column("updated_at", DateTime, default=timezone.now, onupdate=timezone.now),
)


Money = Table(
    "money",
    metadata,
    Column("id", Integer, primary_key=True, unique=True),
    Column("code", String(10)),
    Column("name", String(50)),
    Column("quantity", DECIMAL),
    Column("created_at", DateTime, default=timezone.now),
    Column("updated_at", DateTime, default=timezone.now, onupdate=timezone.now),
)


CurrencyHistory = Table(
    "currency_history",
    metadata,
    Column("id", Integer, primary_key=True, unique=True, autoincrement=True),
    Column("currency_id", Integer, ForeignKey("currency.id")),
    Column("price", DECIMAL),
    Column("created_at", DateTime, default=timezone.now),
)
