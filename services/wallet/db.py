from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (TIMESTAMP, Column, Float, MetaData, String, Table)
from configs.config import getSettings
import databases


settings = getSettings()

database = databases.Database(settings.DATABASE_URL)
currency_database = databases.Database(settings.CURRENCY_DATABASE_URL)
metadata = MetaData()
currencyMetadata = MetaData()


Wallet = Table(
    'wallet',
    metadata,
    Column(UUID(as_uuid=True), name='user_id'),
    Column(UUID(as_uuid=True), name='currency_id'),
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
    Column('quantity', Float, nullable=False),
    Column('market_cap', Float, nullable=False),
)

