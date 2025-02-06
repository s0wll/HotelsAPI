from sqlalchemy import select

from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room



class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room


    async def get_all(self, hotel_id) -> list[Room]:
        query = select(RoomsOrm).filter_by(hotel_id=hotel_id)
        result = await self.session.execute(query)

        return [Room.model_validate(room, from_attributes=True) for room in result.scalars().all()]