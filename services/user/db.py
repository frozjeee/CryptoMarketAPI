from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (
    TIMESTAMP, Boolean, Column, Date, 
    Integer, MetaData, String, Table
)
from configs.config import getSettings
import databases


settings = getSettings()

database = databases.Database(settings.DATABASE_URL)
metadata = MetaData()


User = Table(
    'user',
    metadata,
    Column('id', UUID, primary_key=True, unique=True, nullable=False),
    Column('is_superuser', Boolean, default=True, nullable=False),
    Column('email', String(250), unique=True, nullable=False),
    Column('name', String(250), nullable=False),
    Column('password', String(250), nullable=False),
    Column('birthdate', Date, nullable=False),
    Column('country_id', Integer, nullable=False),
    Column('verified', Boolean, nullable=False),
    Column('main_currency', String(10), nullable=False),
    Column('created_at', TIMESTAMP, nullable=False),
    Column('updated_at', TIMESTAMP, nullable=False)
)
