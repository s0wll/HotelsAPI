'''Основной файл для подключения базы данных'''
'''ORM - общее название для фреймворков или библиотек, позволяющих автоматически связать базу данных с кодом'''

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine  # 1 - , 2 - Асинхронный движок

from src.config import settings


engine = create_async_engine(settings.DB_URL)

async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)  # Для создания сессии (отправление транзакции).
                                                                               # Объект сессии (которые мы будем создавать) - своего рода транзакция в базу данных
session = async_session_maker()
await session.execute()  # Функция для исполнения запросов