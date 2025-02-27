from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.services.facilities import FacilitiesService
from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd


router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
@cache(expire=10)
async def get_facilities(db: DBDep):
    print("иду в бд")
    return await db.facilities.get_all()


@router.post("")
async def create_facility(db: DBDep, facility_data: FacilityAdd = Body()):
    facility = await FacilitiesService(db).create_facility(facility_data)
    return {"status": "OK", "data": facility}
