from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.country.models import Country


async def getCountry(db: AsyncSession, id: int):
    q = select(Country).filter(Country.id == id)
    cur = await db.execute(q)
    return cur.scalar_one_or_none()


async def getAllCountries(db: AsyncSession):
    q = select(Country)
    cur = await db.execute(q)
    return cur.scalars().all()
