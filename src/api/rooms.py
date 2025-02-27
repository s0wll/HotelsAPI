from datetime import date

from fastapi import APIRouter, Body, Query
from fastapi_cache.decorator import cache

from src.services.rooms import RoomsService
from src.exceptions import HotelNotFoundException, HotelNotFoundHTTPException, RoomNotFoundException, RoomNotFoundHTTPException
from src.api.dependencies import DBDep
from src.schemas.rooms import RoomAddRequest, RoomPatchRequest


router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")  # Ручка на получение доступных для брони номеров в отеле
@cache(expire=10)
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(example="2025-02-07"),
    date_to: date = Query(example="2025-02-09"),
):
    try:
        return await RoomsService(db).get_filtered_by_time(hotel_id, date_from, date_to)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException


@router.get("/{hotel_id}/rooms/{room_id}")
@cache(expire=10)
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    try:
        return await RoomsService(db).get_room(hotel_id, room_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
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
        room = await RoomsService(db).create_room(hotel_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(
    hotel_id: int,
    room_id: int,
    room_data: RoomAddRequest,
    db: DBDep,
):
    try:
        await RoomsService(db).edit_room(hotel_id, room_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def partially_edit_room(
    hotel_id: int,
    room_id: int,
    room_data: RoomPatchRequest,
    db: DBDep,
):
    try:
        await RoomsService(db).partially_edit_room(hotel_id, room_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    try:
        await RoomsService(db).delete_room(hotel_id, room_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    return {"status": "OK"}
