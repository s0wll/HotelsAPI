# API ручки для /users(endpoints)
from fastapi import APIRouter, Response

from src.exceptions import IncorrectPasswordException, IncorrectPasswordHTTPException, UserAlreadyExistsException, UserEmailAlreadyExistsHTTPException, UserEmailNotFoundException, UserNotFoundException
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
        user_access_token = await AuthService(db).login_user(data, response)
    except UserNotFoundException:
        raise UserEmailNotFoundException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException
    return {"access_token": user_access_token}


@router.get("/me")  # Ручка на получение данных аутентифицированного пользователя (id)
async def get_me(user_id: UserIdDep, db: DBDep):
    user = await AuthService(db).get_me(user_id)
    return user


@router.post("/logout")
async def logout(response: Response):
    await AuthService().logout(response)
    return {"status": "OK"}
