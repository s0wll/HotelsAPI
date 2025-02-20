import json
import pytest
from httpx import AsyncClient

from src.main import app
from src.database import Base, engine_null_pool
from src.models import *
from src.config import settings
from src.utils.db_manager import DBManager
from src.database import async_session_maker_null_pool
from src.schemas.hotels import HotelAdd
from schemas.rooms import RoomAdd


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"
    assert settings.DB_NAME == "test"


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open("tests/mock_hotels.json") as file:
        hotels_data = json.load(file)
        for hotel in hotels_data:
            hotel_data = HotelAdd(**hotel)
            async with DBManager(session_factory=async_session_maker_null_pool) as db:
                await db.hotels.add(hotel_data)
                await db.commit()

    with open("tests/mock_rooms.json") as file:
        rooms_data = json.load(file)
        for room in rooms_data:
            room_data = RoomAdd(**room)
            async with DBManager(session_factory=async_session_maker_null_pool) as db:
                await db.rooms.add(room_data)
                await db.commit()
    

@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post(
            "/auth/register",
            json={
                "email": "mark@gmail.com",
                "password": "12345"
            }
        )
