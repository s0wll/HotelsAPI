"""Основной файл для подключения базы данных"""

"""ORM - общее название для фреймворков или библиотек, позволяющих автоматически связать базу данных с кодом,"""
"""чтобы программист не заморачивался с таблицами и тд, а работал с БД через код"""
# ruff: noqa: E402
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)  # 1 - класс для создания сессии (отправление транзакции), 2 - Асинхронный движок
from sqlalchemy.orm import DeclarativeBase  # Библиотека алхимии ОРМ (для работы с БД через код)

from src.config import settings

db_params = {}
if settings.MODE == "TEST":
    db_params = {"poolclass": NullPool}

engine = create_async_engine(settings.DB_URL, **db_params)

async_session_maker = async_sessionmaker(
    bind=engine, expire_on_commit=False
)  # Для создания сессии (отправление транзакции).
# Объект сессии (которые мы будем создавать) - своего рода транзакция в базу данных


class Base(
    DeclarativeBase
):  # Создаем класс, который ничего не делает. Он нужен, чтобы мы наследовали от него все модели в проекте
    pass
