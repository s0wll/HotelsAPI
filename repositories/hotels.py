from sqlalchemy import select, func

from repositories.base import BaseRepository
from models.hotels import HotelsOrm


class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(
            self, 
            title,
            location,
            limit,
            offset,
        ):
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

        return result.scalars().all() 
