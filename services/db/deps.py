from typing import Generator

from services.db.db import Session


async def get_db_session() -> Generator:
    try:
        async with Session() as session:
            yield session
    finally:
        await Session.remove()
