from sqlalchemy import select, insert
from pydantic import BaseModel


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)  # stmt (statement - выражение) используется для всего кроме select, т.к. select - запрос на выборку данных, который возвращает результат, поэтому нужно называть query 
        result = await self.session.execute(query)
        return result.scalars().all() 

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none() 
    
    async def add(self, data: BaseModel):
        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_data_stmt)
        return result.scalars().one()

