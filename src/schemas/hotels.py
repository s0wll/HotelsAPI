from pydantic import BaseModel, Field

class Hotel(BaseModel):  # Класс Hotel для удобного использования данных в коде (принцип dry). BaseModel - класс библиотеки Pydantic
    title: str
    location: str

class HotelPATCH(BaseModel):
    title: str | None = Field(None)
    location: str | None = Field(None) 