from services.db.db import db
from services.currency.models import Currency
from services.currency.schemas import CurrencyIn, CurrencyUpdate


async def createCurrency(currencyIn: CurrencyIn):
    currencyIn.market_cap = currencyIn.quantity * currencyIn.price
    query = Currency.insert().values(currencyIn.dict())
    await db.execute(query=query)


async def getCurrency(currencyId):
    query = Currency.select().where(Currency.c.id == currencyId)
    return await db.fetch_one(query=query)


async def getCurrencies():
    query = Currency.select()
    return await db.fetch_all(query)


async def updateCurrency(currency: CurrencyUpdate):
    query = (
        Currency.update()
        .where(Currency.c.id == currency.id)
        .values(currency.dict(exclude_none=True))
    )
    await db.execute(query=query)


async def deleteCurrency(currencyId: int):
    query = Currency.delete().where(Currency.c.id == currencyId)
    await db.execute(query=query)
