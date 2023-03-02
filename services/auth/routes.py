from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from services.auth import crud
from services.user.crud import getUserByEmail, createUser
from services.user.schemas import UserIn


router = APIRouter()


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(userCredentials: OAuth2PasswordRequestForm = Depends()):
    user = await getUserByEmail(userCredentials.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User does not exist"
        )
    accessToken = crud.createAccessToken(user)

    return {"access_token": accessToken, "token_type": "Bearer"}


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(userIn: UserIn):
    user = await getUserByEmail(userIn.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists"
        )

    return await createUser(userIn=userIn)
