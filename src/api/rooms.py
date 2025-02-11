from datetime import date
from fastapi import APIRouter, Body, Query

from src.api.dependencies import DBDep
from src.schemas.rooms import Room, RoomAdd, RoomAddRequest, RoomPatchRequest, RoomPatch
from src.schemas.facilities import RoomFacilityAdd


router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")  # Ручка на получение доступных для брони номеров в отеле
async def get_rooms(
        hotel_id: int, 
        db: DBDep,
        date_from: date = Query(example="2025-02-07"),
        date_to: date = Query(example="2025-02-09"),
):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from = date_from, date_to=date_to)
    

@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms")
async def create_room(db: DBDep, hotel_id: int, room_data: RoomAddRequest = Body(
    openapi_examples={
        "1": {"summary": "Эконом", "value": {
            "title": "Эконом номер",
            "description": "Односпальный номер",
            "price": 1000,
            "quantity": 5,
            "facilities_ids": [1, 2],
        }},
        "2": {"summary": "Люкс", "value": {
            "title": "Люкс номер",
            "description": "Двуспальный номер",
            "price": 4000,
            "quantity": 2,
            "facilities_ids": [1, 2],
        }},
}
)):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)

    rooms_facilities_data = [RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids]
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
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(_room_data, id=room_id)

    current_facilities_data = await db.rooms_facilities.get_filtered(room_id=room_id)
    current_facilities_ids = [current_facilities_data[i].facility_id for i in range(len(current_facilities_data))]
    
    for current_facility_id in current_facilities_ids:
        if room_data.facilities_ids.count(current_facility_id) == 0:
            await db.rooms_facilities.delete(facility_id=current_facility_id, room_id=room_id)
        if room_data.facilities_ids.count(current_facility_id) > 0:
            room_data.facilities_ids.remove(current_facility_id)
        
    if room_data.facilities_ids:
        rooms_facilities_data = [RoomFacilityAdd(room_id=room_id, facility_id=f_id) for f_id in room_data.facilities_ids]
        await db.rooms_facilities.add_bulk(rooms_facilities_data)
        
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def partially_edit_room(
        hotel_id: int, 
        room_id: int, 
        room_data: RoomPatchRequest,
        db: DBDep,
):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    await db.rooms.edit(_room_data, exclude_unset=True, hotel_id=hotel_id, id=room_id)

    current_facilities_data = await db.rooms_facilities.get_filtered(room_id=room_id)
    current_facilities_ids = [current_facilities_data[i].facility_id for i in range(len(current_facilities_data))]
    
    for current_facility_id in current_facilities_ids:
        if room_data.facilities_ids.count(current_facility_id) == 0:
            await db.rooms_facilities.delete(facility_id=current_facility_id, room_id=room_id)
        if room_data.facilities_ids.count(current_facility_id) > 0:
            room_data.facilities_ids.remove(current_facility_id)
        
    if room_data.facilities_ids:
        rooms_facilities_data = [RoomFacilityAdd(room_id=room_id, facility_id=f_id) for f_id in room_data.facilities_ids]
        await db.rooms_facilities.add_bulk(rooms_facilities_data)

    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    await db.rooms.delete(hotel_id=hotel_id, id=room_id)
    await db.commit()
    return {"status": "OK"}