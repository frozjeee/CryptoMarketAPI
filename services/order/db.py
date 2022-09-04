from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (TIMESTAMP, Column, Float, Integer, MetaData, String, Table)
from configs.config import getSettings
import uuid
import databases
import sqlalchemy.types as types


settings = getSettings()

database = databases.Database(settings.DATABASE_URL)
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


Order = Table(
    'order',
    metadata,
    Column(UUID(as_uuid=True), name='id', primary_key=True, default=uuid.uuid4(), unique=True),
    Column(UUID(as_uuid=True), name='user_id', default=uuid.uuid4()),
    Column(UUID(as_uuid=True), name='currency_id', default=uuid.uuid4()),
    Column('type', OrderType, nullable=False),
    Column('price', Float, nullable=False),
    Column('quantity', Float, nullable=False),
    Column('status', OrderStatus, nullable=False),
    Column('ordered_at', TIMESTAMP, nullable=False, default=datetime.today())
)


