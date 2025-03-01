# API ручки для /users(endpoints)
from fastapi import APIRouter, Response

from src.exceptions import (
    IncorrectPasswordException,
    IncorrectPasswordHTTPException,
    UserAlreadyExistsException,
    UserEmailAlreadyExistsHTTPException,
    UserEmailNotFoundException,
    UserNotFoundException,
)
from src.api.dependencies import UserIdDep, DBDep
from src.services.auth import AuthService
from src.schemas.users import UserRequestAdd


router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(
    data: UserRequestAdd,
    db: DBDep,
):
    try:
        await AuthService(db).register_user(data)
    except UserAlreadyExistsException:
        raise UserEmailAlreadyExistsHTTPException
    return {"status": "OK"}


@router.post("/login")
async def login_user(
    data: UserRequestAdd,
    response: Response,
    db: DBDep,
):
    try:
        access_token = await AuthService(db).login_user(data)
    except UserNotFoundException:
        raise UserEmailNotFoundException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.get("/me")  # Ручка на получение данных аутентифицированного пользователя (id)
async def get_me(user_id: UserIdDep, db: DBDep):
    return await AuthService(db).get_one_or_none_user(user_id)


@router.post("/logout")
async def logout(response: Response):
    await AuthService().logout(response)
    return {"status": "OK"}
