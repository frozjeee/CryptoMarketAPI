from typing import List
from pathlib import Path

from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

from services.user.models import User
from services.db.deps import get_db_session
from services.auth.deps import getAdminUser
from services.currency import crud as curr_crud, schemas as curr_schemas
from services.order import crud as ord_crud, schemas as ord_schemas
from services.wallet import crud as wall_crud, schemas as wall_schemas


router = APIRouter()
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(Path(BASE_DIR, "../templates")))


@router.get("/dashboard/", response_class=HTMLResponse)
async def dashboardView(
    request: Request,
    db: AsyncSession = Depends(get_db_session)
):
    currs = await curr_crud.getCurrencies(db, 5)
    return templates.TemplateResponse("dashboard.html", {"request": request, "currencies": currs})


@router.get("/login/", response_class=HTMLResponse)
async def loginView(
    request: Request,
    db: AsyncSession = Depends(get_db_session)
):
    # wasd = await crud.getCurrencies(db)
    return templates.TemplateResponse("login.html", {"request": request, "title": "HELLO"})


@router.get("/register/", response_class=HTMLResponse)
async def registerView(
    request: Request,
    db: AsyncSession = Depends(get_db_session)
):
    # wasd = await crud.getCurrencies(db)
    return templates.TemplateResponse("register.html", {"request": request, "title": "HELLO"})


@router.get("/orders/", response_class=HTMLResponse)
async def ordersView(
    request: Request,
    db: AsyncSession = Depends(get_db_session)
):
    # orders = await ord_crud.getOrders(db)
    return templates.TemplateResponse("orders.html", {"request": request})


@router.get("/currencies/", response_class=HTMLResponse)
async def currenciesView(
    request: Request,
    db: AsyncSession = Depends(get_db_session)
):
    currs = await curr_crud.getCurrencies(db, None)
    return templates.TemplateResponse("currencies.html", {"request": request, "currencies": currs})


@router.get("/currency/{id}", response_class=HTMLResponse)
async def currencyView(
    request: Request,
    *,
    db: AsyncSession = Depends(get_db_session),
    id: int
):
    currency = await curr_crud.getCurrency(db, id)
    return templates.TemplateResponse("currency.html", {"request": request, "currency": currency})


@router.get("/verify/", response_class=HTMLResponse)
async def verifyView(
    request: Request,
    *,
    db: AsyncSession = Depends(get_db_session),
):
    return templates.TemplateResponse("verify.html", {"request": request})


@router.get("/view/user/", response_class=HTMLResponse)
async def userView(
    request: Request
):
    return templates.TemplateResponse("user.html", {"request": request})


# @router.get("/{path:path}")
# async def catch_all_handler(path: str):
#     return {"message": f"You requested the path: /{path}"}