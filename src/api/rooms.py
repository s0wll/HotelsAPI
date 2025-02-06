from fastapi import APIRouter, Body

from src.repositories.rooms import RoomsRepository
from src.database import async_session_maker
from src.schemas.rooms import RoomAdd, RoomPATCH


router = APIRouter(prefix="/rooms", tags=["Номера"])


@router.get("/{hotel_id}")
async def get_rooms(hotel_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(hotel_id=hotel_id)
    

@router.get("/{hotel_id}/{room_id}")
async def get_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(hotel_id=hotel_id, id=room_id)


@router.post("/{hotel_id}")
async def create_room(room_data: RoomAdd = Body(openapi_examples={
        "1": {"summary": "Эконом", "value": {
            "hotel_id": 11,
            "title": "Эконом номер",
            "description": "Односпальный номер без кондиционера",
            "price": 1000,
            "quantity": 5,
        }},
        "2": {"summary": "Люкс", "value": {
            "hotel_id": 29,
            "title": "Люкс номер",
            "description": "Двуспальный номер с кондиционером и телеком",
            "price": 4000,
            "quantity": 2,
        }},
}),
):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(room_data)
        await session.commit()
    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/{room_id}")
async def edit_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomAdd,
):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, hotel_id=hotel_id, id=room_id)
        await session.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/{room_id}")
async def partially_edit_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomPATCH,
):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, exclude_unset=True, hotel_id=hotel_id, id=room_id)
        await session.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/{room_id}")
async def delete_room(
        hotel_id: int,
        room_id: int,
):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(hotel_id=hotel_id, id=room_id)
        await session.commit()
    return {"status": "OK"}