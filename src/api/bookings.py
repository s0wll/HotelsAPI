from fastapi import APIRouter, Body, HTTPException
from fastapi_cache.decorator import cache

from src.exceptions import AllRoomsAreBookedException, ObjectNotFoundException
from src.schemas.hotels import Hotel
from src.schemas.rooms import Room
from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAddRequest, BookingAdd


router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("")
@cache(expire=10)
async def get_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me")
@cache(expire=10)
async def get_my_bookings(user_id: UserIdDep, db: DBDep):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post("")
async def add_booking(
    user_id: UserIdDep,
    db: DBDep,
    booking_data: BookingAddRequest = Body(),
):
    try:
        room_data: Room = await db.rooms.get_one(id=booking_data.room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=400, detail="Номер не найден")
    hotel_data: Hotel = await db.hotels.get_one(id=room_data.hotel_id)
    room_price: int = room_data.price

    _booking_data = BookingAdd(
        user_id=user_id,
        price=room_price,
        **booking_data.model_dump(),
    )

    try:
        booking = await db.bookings.add_booking(_booking_data, hotel_id=hotel_data.id)
    except AllRoomsAreBookedException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)
    await db.commit()
    return {"status": "OK", "data": booking}
