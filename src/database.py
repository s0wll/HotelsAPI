'''Основной файл для подключения базы данных'''

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine  # 1 - , 2 - Асинхронный движок
from sqlalchemy import text
import asyncio

from src.config import settings


engine = create_async_engine(settings.DB_URL)

async def func():
    async with engine.begin() as conn:
        res = await conn.execute(text("SELECT version()"))
        print(res.fetchone())

asyncio.run(func())