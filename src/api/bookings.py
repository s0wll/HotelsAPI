from fastapi import APIRouter, Body


from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAddRequest, BookingAdd


router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("")
async def add_booking(
    user_id: UserIdDep,
    db: DBDep,
    booking_data: BookingAddRequest = Body(),
):
    room_data = await db.rooms.get_one_or_none(id=booking_data.room_id)
    room_price: int = room_data.price

    _booking_data = BookingAdd(
        user_id=user_id,
        price=room_price,
        **booking_data.model_dump(),
    )

    booking = await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "OK", "data": booking}