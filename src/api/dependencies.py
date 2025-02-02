from typing import Annotated

from fastapi import Depends, Query
from pydantic import BaseModel


class PaginationParams(BaseModel):  # 1 - дефолт значение у переменной (deafult: 1). Для per_page дефолт None, но в запросе в БД либо пользователь передает, либо будет дефолт 5
    page: Annotated[int | None, Query(1, ge=1, description="Номер страницы")]  # Пагинация  # gt и lt - это ограничения, которые можно указать для параметра (greaterthan lessthen). ge - >=
                                                                                      # Таким образом мы делаем валидацию Pydantic (FastAPI уже вшил ее, поэтому можно исп gt и lt) для пагинации
    per_page: Annotated[int | None, Query(None, ge=1, lt=30, description="Количество отелей на одной странице")]  # Пагинация


PaginationDep = Annotated[PaginationParams, Depends()]