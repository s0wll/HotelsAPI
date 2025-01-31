from pydantic import BaseModel, Field

class Hotel(BaseModel):  # Класс Hotel для удобного использования данных в коде (принцип dry). BaseModel - класс библиотеки Pydantic
    title: str
    name: str

class HotelPATCH(BaseModel): 
    title: str | None = Field(None)
    name: str | None = Field(None) 