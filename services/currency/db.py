from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (TIMESTAMP, Column, Float, 
    ForeignKey, Integer, MetaData, String, Table)
from configs.config import getSettings
import databases


settings = getSettings()

database = databases.Database(settings.DATABASE_URL)

metadata = MetaData()


Currency = Table(
    'currency',
    metadata,
    Column(UUID(as_uuid=True), name='id', primary_key=True, nullable=False, unique=True, default=uuid4()),
    Column('code', String(10), nullable=False),
    Column('name', String(50), nullable=False),
    Column('price', Float, nullable=False),
    Column('quantity', Float, nullable=False),
    Column('market_cap', Float, nullable=False),
)


CurrencyHistory = Table(
    'currency_history',
    metadata,
    Column('id', Integer, primary_key=True, unique=True, autoincrement=True),
    Column('currency_id', ForeignKey('currency.id'), nullable=False),
    Column('price', Float, nullable=False),
    Column('time', TIMESTAMP, nullable=False)
)


Tick = Table(
    'tick',
    metadata,
    Column('id', Integer, primary_key=True, unique=True, autoincrement=True),
    Column('currency_id', ForeignKey('currency.id'), nullable=False),
    Column('tick_price', Float, nullable=False),
    Column('time', TIMESTAMP, nullable=False)
)

