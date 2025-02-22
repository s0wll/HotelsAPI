# Создание модели sqlalchemy (в БД это таблица)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from src.database import Base


class HotelsOrm(Base):  # Класс модели отелей для работы с БД
    __tablename__ = "hotels"  # Название таблицы

    #  Атрибуты класса (модели отелей), которые соответствуют столбцам таблицы в БД
    id: Mapped[int] = mapped_column(
        primary_key=True
    )  # primary_key - как в SQL, означает что значения в колонке уникальны, столбец id является первичным ключом
    title: Mapped[str] = mapped_column(
        String(100)
    )  # String(100) == String(length=100) (Ограничение по длине title)
    location: Mapped[
        str
    ]  # Т.к. нет ограничений по кол-ву символов, то тут не используем mapped_column()
