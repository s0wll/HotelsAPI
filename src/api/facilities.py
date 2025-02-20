from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.init import redis_connector
from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd
from src.tasks.tasks import test_task


router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
@cache(expire=10)
async def get_facilities(db: DBDep):
    print("иду в бд")
    return await db.facilities.get_all()
    


@router.post("")
async def create_facility(db: DBDep, facility_data: FacilityAdd = Body()):
    facility = await db.facilities.add(facility_data)
    await db.commit()

    test_task.delay()
    
    return {"status": "OK", "data": facility}
