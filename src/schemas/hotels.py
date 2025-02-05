from pydantic import BaseModel, Field, ConfigDict

class HotelAdd(BaseModel):  # Класс Hotel для удобного использования данных в коде (принцип dry). BaseModel - класс библиотеки Pydantic
    title: str
    location: str

class Hotel(HotelAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)

class HotelPATCH(BaseModel):
    title: str | None = Field(None)
    location: str | None = Field(None) 