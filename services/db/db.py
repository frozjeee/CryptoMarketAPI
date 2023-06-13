from asyncio import current_task

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from config.config import settings


Model = declarative_base()

engine = create_async_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=False,
)

Session = async_scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine,  expire_on_commit=False, class_=AsyncSession),
    scopefunc=current_task
)
