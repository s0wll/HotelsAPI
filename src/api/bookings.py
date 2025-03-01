from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.services.bookings import BookingsService
from src.exceptions import (
    AllRoomsAreBookedException,
    AllRoomsAreBookedHTTPException,
    RoomNotFoundException,
    RoomNotFoundHTTPException,
)
from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAddRequest


router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("")
@cache(expire=10)
async def get_bookings(db: DBDep):
    return await BookingsService(db).get_bookings()


@router.get("/me")
@cache(expire=10)
async def get_my_bookings(user_id: UserIdDep, db: DBDep):
    return await BookingsService(db).get_my_bookings(user_id)


@router.post("")
async def add_booking(
    user_id: UserIdDep,
    db: DBDep,
    booking_data: BookingAddRequest = Body(),
):
    try:
        booking = await BookingsService(db).add_booking(user_id, booking_data)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except AllRoomsAreBookedException:
        raise AllRoomsAreBookedHTTPException
    return {"status": "OK", "data": booking}
