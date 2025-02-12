# Pydantic Схема для данных для hotels
from pydantic import BaseModel, ConfigDict

class HotelAdd(BaseModel):  # Класс Hotel для удобного использования данных в коде (принцип dry). BaseModel - класс библиотеки Pydantic
    title: str
    location: str

class Hotel(HotelAdd):
    id: int

class HotelPATCH(BaseModel):
    title: str | None = None
    location: str | None = None