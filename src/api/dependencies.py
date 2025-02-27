# Файл с зависимостями
from typing import Annotated

from fastapi import Depends, Query, Request
from pydantic import BaseModel

from src.exceptions import IncorrectTokenException, IncorrectTokenHTTPException, NotAuthenticatedHTTPException
from services.auth import AuthService
from src.utils.db_manager import DBManager
from src.database import async_session_maker


class PaginationParams(
    BaseModel
):  # 1 - дефолт значение у переменной (deafult: 1). Для per_page дефолт None, но в запросе в БД либо пользователь передает, либо будет дефолт 5
    page: Annotated[
        int | None, Query(1, ge=1, description="Номер страницы")
    ]  # Пагинация  # gt и lt - это ограничения, которые можно указать для параметра (greaterthan lessthen). ge - >=
    # Таким образом мы делаем валидацию Pydantic (FastAPI уже вшил ее, поэтому можно исп gt и lt) для пагинации
    per_page: Annotated[
        int | None, Query(None, ge=1, lt=30, description="Количество отелей на одной странице")
    ]  # Пагинация


PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request) -> str:  # Ф-я получения токена пользователя
    token = request.cookies.get("access_token", None)
    if not token:
        raise NotAuthenticatedHTTPException
    return token


def get_current_user_id(
    token: str = Depends(get_token),
) -> int:  # Ф-я получения айди текущего аутентифицированного пользователя по токену
    try:
        data = AuthService().decode_token(token)
    except IncorrectTokenException:
        raise IncorrectTokenHTTPException
    return data["user_id"]


UserIdDep = Annotated[int, Depends(get_current_user_id)]


async def get_db():  # Генератор, который открывает контекстный дб менеджер и отдавать сущность дб менеджера
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
