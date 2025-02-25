from datetime import date
from fastapi import APIRouter, Body, Query
from fastapi_cache.decorator import cache

from src.exceptions import HotelNotFoundHTTPException, ObjectNotFoundException, RoomNotFoundHTTPException, check_date_to_after_date_from
from src.api.dependencies import DBDep
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatchRequest, RoomPatch
from src.schemas.facilities import RoomFacilityAdd


router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")  # Ручка на получение доступных для брони номеров в отеле
@cache(expire=10)
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(example="2025-02-07"),
    date_to: date = Query(example="2025-02-09"),
):
    check_date_to_after_date_from(date_from, date_to)
    return await db.rooms.get_filtered_by_time(
        hotel_id=hotel_id, date_from=date_from, date_to=date_to
    )


@router.get("/{hotel_id}/rooms/{room_id}")
@cache(expire=10)
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    room = await db.rooms.get_one_or_none_with_rels(id=room_id, hotel_id=hotel_id)
    if not room:
        raise RoomNotFoundHTTPException


@router.post("/{hotel_id}/rooms")
async def create_room(
    db: DBDep,
    hotel_id: int,
    room_data: RoomAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "Эконом",
                "value": {
                    "title": "Эконом номер",
                    "description": "Односпальный номер",
                    "price": 1000,
                    "quantity": 5,
                    "facilities_ids": [1],
                },
            },
            "2": {
                "summary": "Люкс",
                "value": {
                    "title": "Люкс номер",
                    "description": "Двуспальный номер",
                    "price": 4000,
                    "quantity": 2,
                    "facilities_ids": [1, 2, 3],
                },
            },
        }
    ),
):
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)

    rooms_facilities_data = [
        RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids
    ]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()
    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(
    hotel_id: int,
    room_id: int,
    room_data: RoomAddRequest,
    db: DBDep,
):
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
    try:
        await db.rooms.get_one(id=room_id)
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(_room_data, id=room_id)
    await db.rooms_facilities.set_room_facilities(room_id, facilities_ids=room_data.facilities_ids)
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def partially_edit_room(
    hotel_id: int,
    room_id: int,
    room_data: RoomPatchRequest,
    db: DBDep,
):
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
    try:
        await db.rooms.get_one(id=room_id)
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException
    _room_data_dict = room_data.model_dump(exclude_unset=True)
    _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)
    await db.rooms.edit(_room_data, exclude_unset=True, hotel_id=hotel_id, id=room_id)
    if "facilities_ids" in _room_data_dict:
        await db.rooms_facilities.set_room_facilities(
            room_id, facilities_ids=_room_data_dict["facilities_ids"]
        )
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
    try:
        await db.rooms.get_one(id=room_id)
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException
    await db.rooms.delete(hotel_id=hotel_id, id=room_id)
    await db.commit()
    return {"status": "OK"}
