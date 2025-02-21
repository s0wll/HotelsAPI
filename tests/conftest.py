import json
from unittest import mock

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()  # мок для редис кэша, чтобы при тестировании не было ошибок с внешним redis cache

import pytest
from httpx import AsyncClient

from src.main import app
from src.database import Base, engine
from src.models import *
from src.config import settings
from src.utils.db_manager import DBManager
from src.database import async_session_maker
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"
    assert settings.DB_NAME == "test"


@pytest.fixture(scope="function")
async def db() -> DBManager:  # type: ignore
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


@pytest.fixture(scope="module")
async def db_module() -> DBManager:  # type: ignore
    async with DBManager(session_factory=async_session_maker) as db_module:
        yield db_module


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open("tests/mock_hotels.json", encoding="utf-8") as file_hotels:
        hotels_json_data = json.load(file_hotels)
    with open("tests/mock_rooms.json", encoding="utf-8") as file_rooms:
        rooms_json_data = json.load(file_rooms)

    hotels_data = [HotelAdd.model_validate(hotel_json_data) for hotel_json_data in hotels_json_data]   
    rooms_data = [RoomAdd.model_validate(room_json_data) for room_json_data in rooms_json_data]

    async with DBManager(session_factory=async_session_maker) as db_:
        await db_.hotels.add_bulk(hotels_data)
        await db_.rooms.add_bulk(rooms_data)
        await db_.commit()


@pytest.fixture(scope="session")
async def ac() -> AsyncClient:  # type: ignore
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def register_user(ac, setup_database):
    await ac.post(
        "/auth/register",
        json={
            "email": "mark@gmail.com",
            "password": "12345"
        }
    )


@pytest.fixture(scope="session", autouse=True)
async def authentificated_ac(ac, register_user):
    await ac.post(
        "/auth/login",
        json={
            "email": "mark@gmail.com",
            "password": "12345"
        }
    )
    assert ac.cookies["access_token"]
    yield ac


