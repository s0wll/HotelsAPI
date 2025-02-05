# API ручки для /users(endpoints)
from fastapi import APIRouter

from repositories.users import UsersRepository
from src.database import async_session_maker
from schemas.users import UserRequestAdd, UserAdd

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])
                   

@router.post("/register")
async def register_user(
    data: UserRequestAdd,
):
    hashed_password = "343434djsjfhwdjwbc"  # Реализуем позже
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session: 
        await UsersRepository(session).add(new_user_data)
        await session.commit()

    return {"status": "OK"}