from src.schemas.hotels import Hotel
from src.exceptions import AllRoomsAreBookedException, ObjectNotFoundException, RoomNotFoundException, UserAlreadyExistsException
from src.schemas.rooms import Room
from src.schemas.bookings import BookingAdd, BookingAddRequest
from src.api.dependencies import UserIdDep
from src.services.base import BaseService


class BookingsService(BaseService):
    async def get_bookings(self):
        return await self.db.bookings.get_all()
    
    async def get_my_bookings(self, user_id: UserIdDep):
        return await self.db.bookings.get_filtered(user_id=user_id)
    
    async def add_booking(
        self,
        user_id: UserIdDep,
        booking_data: BookingAddRequest,
    ):
        try:
            room_data: Room = await self.db.rooms.get_one(id=booking_data.room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException
        hotel_data: Hotel = await self.db.hotels.get_one(id=room_data.hotel_id)
        room_price: int = room_data.price

        _booking_data = BookingAdd(
            user_id=user_id,
            price=room_price,
            **booking_data.model_dump(),
        )

        try:
            booking = await self.db.bookings.add_booking(_booking_data, hotel_id=hotel_data.id)
        except UserAlreadyExistsException as ex:
            raise AllRoomsAreBookedException
        await self.db.commit()
        return booking