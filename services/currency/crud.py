from typing import Optional

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from services.currency.models import Currency
from services.currency.schemas import CurrencyIn, CurrencyUpdate


async def createCurrency(db: AsyncSession, currencyIn: CurrencyIn):
    curr = Currency(**currencyIn.dict())
    db.add(curr)
    await db.commit()
    await db.refresh(curr)
    return curr


async def getCurrencyHistory(db: AsyncSession, id: int):
    # current_time = datetime.utcnow()
    # start_time = current_time - timedelta(hours=24)
    # subquery = Query.from_statement(
    # db.execute(
    #     db.query(
    #         func.row_number().over(
    #             order_by=CurrencyHistory.created_at
    #         ).label("row_number"),
    #         func.date_trunc("hour", CurrencyHistory.created_at).label("hour_trunc"),
    #         CurrencyHistory.price
    #     ).filter(
    #         CurrencyHistory.created_at >= start_time,
    #         CurrencyHistory.created_at <= current_time
    #     ).statement
    #     )
    # ).subquery()

    # q = db.query(
    #     subquery.c.hour_trunc,
    #     subquery.c.price
    # ).filter(
    #     subquery.c.row_number <= 24
    # ).order_by(
    #     subquery.c.hour_trunc.asc(),
    #     subquery.c.row_number.desc()
    # )

    # q = select(Currency).filter(Currency.id == id)
    cur = await db.execute(f"""
    SELECT DISTINCT ON (subquery.hour_trunc) subquery.hour_trunc, subquery.price
    FROM (
        SELECT
            ROW_NUMBER() OVER (PARTITION BY DATE_TRUNC('hour', currency_history.created_at) ORDER BY currency_history.created_at DESC) AS row_number,
            DATE_TRUNC('hour', currency_history.created_at) AS hour_trunc,
            currency_history.price
        FROM currency_history
        WHERE currency_history.created_at >= (CURRENT_TIMESTAMP - INTERVAL '24 hours')
            AND currency_history.created_at <= CURRENT_TIMESTAMP
            AND currency_history.currency_id = {id}
        ) AS subquery
    WHERE subquery.row_number = 1
    ORDER BY subquery.hour_trunc ASC;""")
    return cur


async def getCurrency(db: AsyncSession, id: int):
    q = select(Currency).filter(Currency.id == id)
    cur = await db.execute(q)
    return cur.scalar_one_or_none()


async def getCurrencies(db: AsyncSession, limit: Optional[int] = None):
    q = select(Currency)
    if limit:
        q = q.limit(limit)
    cur = await db.execute(q)
    return cur.scalars().all()


async def updateCurrency(db: AsyncSession, currency: CurrencyUpdate):
    q = update(Currency). \
        filter(Currency.id == currency.id). \
        values(currency.dict(exclude_none=True))
    await db.execute(q)


async def deleteCurrency(db: AsyncSession, id: int):
    q = delete(Currency).filter(Currency.id == id)
    await db.execute(q)
