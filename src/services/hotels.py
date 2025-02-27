from datetime import date

from src.schemas.hotels import Hotel, HotelAdd
from src.exceptions import HotelNotFoundException, ObjectNotFoundException, check_date_to_after_date_from
from src.services.base import BaseService


class HotelsService(BaseService):
    async def get_filtered_by_time(
        self,
        pagination,
        title: str | None,
        location: str | None,
        date_from: date,
        date_to: date,
    ):
        check_date_to_after_date_from(date_from, date_to)
        per_page = pagination.per_page or 5
        return await self.db.hotels.get_filtered_by_time(
            date_from=date_from,
            date_to=date_to,
            title=title,
            location=location,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
        )
        # commit() не нужно вызывать в select, т.к. commit() нужно вызывать когда мы хотим внести изменения в БД и зафиксировать это

    async def get_hotel(self, hotel_id: int):
        return await self.db.hotels.get_one(id=hotel_id)
    
    async def add_hotel(self, hotel_data: HotelAdd):
        hotel = await self.db.hotels.add(hotel_data)
        await self.db.commit()
        return hotel
    
    async def edit_hotel(self, hotel_id: int, hotel_data: HotelAdd):
        await self.db.hotels.edit(hotel_data, id=hotel_id)
        await self.db.commit()

    async def partially_edit_hotel(self, hotel_id: int, hotel_data: HotelAdd):
        await self.db.hotels.edit(hotel_data, id=hotel_id, exclude_unset=True)
        await self.db.commit()

    async def delete_hotel(self, hotel_id: int):
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()

    async def get_hotel_with_check(self, hotel_id: int) -> Hotel:
        try:
            return await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException