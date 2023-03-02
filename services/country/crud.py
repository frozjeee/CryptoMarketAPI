from services.db.db import db
from services.country.models import Country


async def getCountry(countryId: int):
    query = Country.select().where(Country.c.id == countryId)
    return await db.fetch_one(query=query)


async def getAllCountries():
    query = Country.select()
    return await db.fetch_all(query=query)
