# Файл с зависимостями
from typing import Annotated

from fastapi import Depends, Query, HTTPException, Request
from pydantic import BaseModel

from services.auth import AuthService


class PaginationParams(BaseModel):  # 1 - дефолт значение у переменной (deafult: 1). Для per_page дефолт None, но в запросе в БД либо пользователь передает, либо будет дефолт 5
    page: Annotated[int | None, Query(1, ge=1, description="Номер страницы")]  # Пагинация  # gt и lt - это ограничения, которые можно указать для параметра (greaterthan lessthen). ge - >=
                                                                                      # Таким образом мы делаем валидацию Pydantic (FastAPI уже вшил ее, поэтому можно исп gt и lt) для пагинации
    per_page: Annotated[int | None, Query(None, ge=1, lt=30, description="Количество отелей на одной странице")]  # Пагинация


PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request) -> str:  # Ф-я получения токена пользователя
    token = request.cookies.get("access_token", None)
    if not token:
        raise HTTPException(status_code=401, detail="Вы не аутентифицированны/Вы не предоставили токен доступа")
    return token


def get_current_user_id(token: str = Depends(get_token)) -> int:  # Ф-я получения айди текущего аутентифицированного пользователя по токену
    data = AuthService().decode_token(token)
    return data["user_id"]


UserIdDep = Annotated[int, Depends(get_current_user_id)]