from datetime import datetime
from sqlalchemy.dialects.postgresql import id
from sqlalchemy import TIMESTAMP, Column, DECIMAL, MetaData, String, Table, create_engine
from configs.config import getSettings
import sqlalchemy.types as types
import databases
import id


settings = getSettings()

order_database = databases.Database(settings.ORDER_DATABASE_URL)
currency_database = databases.Database(settings.CURR_DATABASE_URL)
wallet_database = databases.Database(settings.CURR_DATABASE_URL)
metadata = MetaData()


class OrderType(types.TypeDecorator):
    orderTypes = ["buy", "sell"]
    impl = types.String
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value not in self.orderTypes:
            raise ValueError("Invalid order type")
        return value

    def process_result_value(self, value, dialect):
        return value


class OrderStatus(types.TypeDecorator):
    orderStatuses = ["pending", "filled", "cancelled"]
    impl = types.String
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value not in self.orderStatuses:
            raise ValueError("Invalid order status")
        return value

    def process_result_value(self, value, dialect):
        return value


Currency = Table(
    "currency",
    metadata,
    Column(id(), name="id", primary_key=True, nullable=False, unique=True),
    Column("code", String(10), nullable=False),
    Column("name", String(50), nullable=False),
    Column("price", DECIMAL, nullable=False),
    Column("quantity", DECIMAL, nullable=False),
    Column("market_cap", DECIMAL, nullable=False),
)

Order = Table(
    "order",
    metadata,
    Column(id(), name="id", primary_key=True, unique=True),
    Column(id(), name="user_id"),
    Column(id(), name="currency_id"),
    Column("type", OrderType, nullable=False),
    Column("price", DECIMAL, nullable=False),
    Column("quantity", DECIMAL, nullable=False),
    Column("status", OrderStatus, nullable=False),
    Column("ordered_at", TIMESTAMP, nullable=False),
)

Wallet = Table(
    "wallet",
    metadata,
    Column(id(), name="user_id"),
    Column(id(), name="currency_id"),
    Column("amount", DECIMAL, nullable=False),
    Column("quantity", DECIMAL, nullable=False),
    Column("created_at", TIMESTAMP, nullable=False),
)
