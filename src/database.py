'''Основной файл для подключения базы данных'''

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine  # 1 - , 2 - Асинхронный движок

from src.config import settings


engine = create_async_engine(settings.DB_URL)
