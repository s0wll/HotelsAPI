import json

from fastapi import APIRouter, Body

from src.init import redis_connector
from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd


router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
async def get_facilities(db: DBDep):
    facilities_from_cache = await redis_connector.get("facilities")
    if not facilities_from_cache:
        print("иду в бд")
        facilities = await db.facilities.get_all()
        facilities_schemas: list[dict] = [f.model_dump() for f in facilities]
        facilities_json = json.dumps(facilities_schemas)
        await redis_connector.set("facilities", facilities_json, expire=10)
        
        return facilities
    else:
        facilities_dicts = json.loads(facilities_from_cache)
        return facilities_dicts
    


@router.post("")
async def create_facility(db: DBDep, facility_data: FacilityAdd = Body()):
    facility = await db.facilities.add(facility_data)
    await db.commit()
    return {"status": "OK", "data": facility}
