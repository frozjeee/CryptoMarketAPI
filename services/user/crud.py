import idanalyzer
import logging

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import EmailStr
from sqlalchemy import select, update, delete
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from config.config import settings
from services.user.models import User
from services.user.schemas import UserInSchema, UserVerify, UserUpdateSchema


logger = logging.getLogger("user:")
pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2Scheme = OAuth2PasswordBearer(tokenUrl="login")


async def getUserByEmail(db: AsyncSession, email: EmailStr):
    q = select(User).filter(User.email == email)
    cur = await db.execute(q)
    return cur.scalar_one_or_none()


async def getUserById(db: AsyncSession, id: int):
    q = select(User).filter(User.id == id).options(joinedload(User.country))
    cur = await db.execute(q)
    return cur.scalar_one_or_none()


async def deleteUser(db: AsyncSession, id: int):
    q = delete(User).filter(User.id == id)
    await db.execute(q)


async def createUser(db: AsyncSession, userIn: UserInSchema):
    userDict = userIn.dict()
    userDict["password"] = pwdContext.hash(userDict["password"])
    user = User(**userDict)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


def verifyPassword(plain_password, hashed_password):
    return pwdContext.verify(plain_password, hashed_password)


async def updateUser(db: AsyncSession, user: UserUpdateSchema):
    user_dict = user.dict(exclude_none=True, exclude_unset=True)
    query = update(User). \
        where(User.id == user.id). \
        values(**user_dict)

    await db.execute(query)
    await db.commit()


async def verifyUser(userVerify: UserVerify):
    try:
        coreapi = idanalyzer.CoreAPI(
            settings.ID_ANALYZER_API_KEY, settings.ID_ANALYZER_REGION
        )
        await userVerify.toBase64()

        coreapi.throw_api_exception(True)
        coreapi.enable_authentication(True, "quick")
        coreapi.verify_expiry(True)
        coreapi.enable_vault(False)
        coreapi.verify_age("18-120")
        coreapi.enable_dualside_check(True)

        response = coreapi.scan(
            document_primary=userVerify.frontPage,
            document_secondary=userVerify.backPage,
            biometric_photo=userVerify.userFace
        )
        if response["authentication"]["score"] < 0.5:
            return False

        if not response["face"]["isIdentical"]:
            return False

    except idanalyzer.APIError as e:
        details = e.args[0]
        logging.error(
            "API error code: {}, message: {}".format(
                details["code"], details["message"]
            )
        )
    except Exception as e:
        logging.error(e)

    return True
