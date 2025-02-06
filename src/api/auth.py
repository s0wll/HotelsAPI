# API ручки для /users(endpoints)
from fastapi import APIRouter, HTTPException, Response

from src.api.dependencies import UserIdDep
from src.services.auth import AuthService
from src.repositories.users import UsersRepository
from src.database import async_session_maker
from schemas.users import UserRequestAdd, UserAdd


router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

 
@router.post("/register")
async def register_user(
        data: UserRequestAdd,
):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session: 
        await UsersRepository(session).add(new_user_data)
        await session.commit()

    return {"status": "OK"}


@router.post("/login")
async def login_user(
    data: UserRequestAdd,
    response: Response,
):
    async with async_session_maker() as session: 
        user = await UsersRepository(session).get_user_with_hashed_password(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail="Польозватель с таким email не зарегестрирован")
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Пароль неверный")
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}
    

@router.get("/me")  # Ручка на получение данных аутентифицированного пользователя (id)
async def get_me(
    user_id: UserIdDep,
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(id=user_id)
        return user
    

@router.post("/logout")
async def logout(
        response: Response,
):
    response.delete_cookie("access_token")
    return {"status": "OK"}