from sqlalchemy import select, func # func общий метод для использования любых функций, которые есть в БД

from src.repositories.base import BaseRepository
from models.hotels import HotelsOrm
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

    async def get_all(
            self, 
            title,
            location,
            limit,
            offset,
        ) -> list[Hotel]:
        query = select(HotelsOrm)  # stmt (statement - выражение) используется для всего кроме select, т.к. select - запрос на выборку данных, который возвращает результат, поэтому нужно называть query 
        if title:
            query = query.filter(func.lower(HotelsOrm.title).contains(title.strip().lower()))  # contains - функция, которая позволяет указать шаблон для поиска (по подстроке)
        if location:
            query = query.filter(func.lower(HotelsOrm.location).contains(location.strip().lower()))
        query = (
            query
            .limit(limit)
            .offset(offset)  # все что выше (с if и дальше) - пагинация с опциональной фильтрацией
        )
            
        # stmt (statement - выражение) используется для всего кроме select, т.к. select - запрос на выборку данных, который возвращает результат, поэтому нужно называть query
        print(query.compile(compile_kwargs={"literal_binds": True}))  # Принт в консоль для дебага (или можно в database.py у объекта engine приписать параметр echo=True)
        result = await self.session.execute(query)

        return [Hotel.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]
