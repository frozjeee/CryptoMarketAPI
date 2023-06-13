from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from services.auth import crud
from services.db.deps import get_db_session
from services.user.crud import getUserByEmail, createUser, verifyPassword
from services.user.schemas import UserInSchema


router = APIRouter()


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    db: AsyncSession = Depends(get_db_session),
    userCredentials: OAuth2PasswordRequestForm = Depends()
):
    user = await getUserByEmail(db, userCredentials.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User does not exist"
        )
    if not verifyPassword(userCredentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Not right password"
        )
    accessToken = crud.createAccessToken(user)

    return {"access_token": accessToken, "token_type": "bearer"}


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    db: AsyncSession = Depends(get_db_session),
    *,
    userIn: UserInSchema
):
    user = await getUserByEmail(db, userIn.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists"
        )

    return await createUser(db, userIn)
