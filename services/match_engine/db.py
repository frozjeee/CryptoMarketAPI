from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (TIMESTAMP, Column, Float, MetaData, String, Table)
from configs.config import getSettings
import sqlalchemy.types as types
import databases
import uuid


settings = getSettings()

order_database = databases.Database(settings.ORDER_DATABASE_URL)
currency_database = databases.Database(settings.CURR_DATABASE_URL)
metadata = MetaData()


class OrderType(types.TypeDecorator):
    orderTypes = ['buy', 'sell']
    impl = types.String
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value not in self.orderTypes:
            raise ValueError('Invalid order type')
        return value

    def process_result_value(self, value, dialect):
        return value


class OrderStatus(types.TypeDecorator):
    orderStatuses = ['pending', 'filled', 'cancelled']
    impl = types.String
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value not in self.orderStatuses:
            raise ValueError('Invalid order status')
        return value

    def process_result_value(self, value, dialect):
        return value


Currency = Table(
    'currency',
    metadata,
    Column(UUID(), name='id', primary_key=True, nullable=False, unique=True),
    Column('code', String(10), nullable=False),
    Column('name', String(50), nullable=False),
    Column('price', Float, nullable=False),
    Column('quantity', Float, nullable=False),
    Column('market_cap', Float, nullable=False),
)

Order = Table(
    'order',
    metadata,
    Column(UUID(), name='id', primary_key=True, unique=True),
    Column(UUID(), name='user_id'),
    Column(UUID(), name='currency_id'),
    Column('type', OrderType, unique=True, nullable=False),
    Column('price', Float, nullable=False),
    Column('quantity', Float, nullable=False),
    Column('status', OrderStatus, nullable=False),
    Column('ordered_at', TIMESTAMP, nullable=False, default=datetime.today())
)