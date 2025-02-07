from fastapi import APIRouter, Body

from src.repositories.rooms import RoomsRepository
from src.database import async_session_maker
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatchRequest, RoomPatch


router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_filtered(hotel_id=hotel_id)
    

@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms")
async def create_room(hotel_id: int, room_data: RoomAddRequest = Body(
    openapi_examples={
        "1": {"summary": "Эконом", "value": {
            "title": "Эконом номер",
            "description": "Односпальный номер без кондиционера",
            "price": 1000,
            "quantity": 5,
        }},
        "2": {"summary": "Люкс", "value": {
            "title": "Люкс номер",
            "description": "Двуспальный номер с кондиционером и телеком",
            "price": 4000,
            "quantity": 2,
        }},
}
)):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(_room_data)
        await session.commit()
    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(hotel_id: int, room_id: int, room_data: RoomAddRequest):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(_room_data, id=room_id)
        await session.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def partially_edit_room(hotel_id: int, room_id: int, room_data: RoomPatchRequest):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(_room_data, exclude_unset=True, hotel_id=hotel_id, id=room_id)
        await session.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(hotel_id=hotel_id, id=room_id)
        await session.commit()
    return {"status": "OK"}