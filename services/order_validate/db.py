from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (TIMESTAMP, Column, Float, Integer, MetaData, String, Table)
from configs.config import getSettings
import uuid
import databases
import sqlalchemy.types as types


settings = getSettings()

wallet_db = databases.Database(settings.WALLET_DATABASE_URL)
order_db = databases.Database(settings.ORDER_DATABASE_URL)
metadata = MetaData()
walletMetadata = MetaData()
currencyMetadata = MetaData()


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


Order = Table(
    'order',
    metadata,
    Column(UUID(), name='id', primary_key=True, unique=True),
    Column(UUID(), name='user_id'),
    Column(UUID(), name='currency_id'),
    Column('type', OrderType, nullable=False),
    Column('price', Float, nullable=False),
    Column('quantity', Float, nullable=False),
    Column('status', OrderStatus, nullable=False),
    Column('ordered_at', TIMESTAMP, nullable=False, default=datetime.today())
)


Wallet = Table(
    'wallet',
    walletMetadata,
    Column(UUID(), name='user_id'),
    Column(UUID(), name='currency_id'),
    Column('quantity', Float, nullable=False),
    Column('created_at', TIMESTAMP, nullable=False)
)


Currency = Table(
    'currency',
    currencyMetadata,
    Column(UUID(as_uuid=True), name='id', primary_key=True, nullable=False, unique=True),
    Column('code', String(10), nullable=False),
    Column('name', String(50), nullable=False),
    Column('price', Float, nullable=False),
    Column('market_cap', Float, nullable=False),
)

