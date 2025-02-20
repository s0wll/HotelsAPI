from datetime import date

from src.schemas.bookings import BookingAdd


async def test_booking_crud(db):
    # Добавление бронирования
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2025, month=1, day=1),
        date_to=date(year=2025, month=1, day=2),
        price=1000,
    )
    new_booking = await db.bookings.add(booking_data)

    # Получение этой брони и удостоверение, что она есть
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert booking
    assert booking.id == new_booking.id
    assert booking.room_id == new_booking.room_id
    assert booking.user_id == new_booking.user_id

    # Изменение брони
    updated_date = date(year=2026, month=1, day=2)
    update_booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2026, month=1, day=1),
        date_to=updated_date,
        price=2000,
    )
    await db.bookings.edit(data=update_booking_data, id=new_booking.id)
    updated_booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert updated_booking
    assert updated_booking.id == new_booking.id
    assert updated_booking.date_to == updated_date

    # Удаление брони
    await db.bookings.delete(id=new_booking.id)
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert not booking
