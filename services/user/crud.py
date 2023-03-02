import idanalyzer

from pydantic import EmailStr

from config.config import settings
from services.user.models import User
from services.user.schemas import UserIn, UserVerify
from services.db.db import db


async def getUserByEmail(email: EmailStr):
    query = User.select().where(User.c.email == email)
    result = await db.fetch_one(query=query)
    return dict(result) if result else None


async def getUserById(UserId: int):
    query = User.select()
    return await db.fetch_one(query=query, values=UserId)


async def deleteUser(userId: int):
    query = User.delete().where(User.c.id == userId)
    await db.execute(query=query)


async def createUser(userIn: UserIn):
    query = User.insert().values(dict(userIn))
    await db.execute(query=query)


async def updateUser(UserUpdate: UserIn, userId: int):
    query = (
        User.update()
        .where(User.c.id == userId)
        .values(UserUpdate.dict(exclude_none=True))
    )
    await db.execute(query=query)


async def verifyUser(userVerify: UserVerify):
    try:
        coreapi = idanalyzer.CoreAPI(
            settings.ID_ANALYZER_API_KEY, settings.ID_ANALYZER_REGION
        )

        coreapi.throw_api_exception(True)
        coreapi.enable_authentication(True, "quick")
        coreapi.verify_expiry(True)
        coreapi.verify_age("18-120")
        coreapi.enable_dualside_check(True)

        response = coreapi.scan(
            document_primary=userVerify.frontPage,
            document_secondary=userVerify.backPage,
            biometric_photo=userVerify.userFace,
        )

        if response["authentication"]["score"] < 0.5:
            return False

        if not response["face"]["isIdentical"]:
            return False

    except idanalyzer.APIError as e:
        details = e.args[0]
        print(
            "API error code: {}, message: {}".format(
                details["code"], details["message"]
            )
        )
    except Exception as e:
        print(e)
    return True
