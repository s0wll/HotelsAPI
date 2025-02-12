from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn

import sys
from pathlib import Path

from src.init import redis_connector

sys.path.append(str(Path(__file__).parent.parent))

from src.api.auth import router as router_auth  # Импорт роутера auth
from src.api.hotels import router as router_hotels
from src.api.rooms import router as router_rooms  
from src.api.bookings import router as router_bookings  
from src.api.facilities import router as router_facilities

@asynccontextmanager
async def lifespan(app: FastAPI):
    # При старте приложения
    await redis_connector.connect()
    yield
    # При выключении/перезагрузке приложения
    await redis_connector.close()


app = FastAPI(lifespan=lifespan)  # Приложение - объект класса FastAPI

app.include_router(router_auth)
app.include_router(router_hotels)  # Подключение роутера hotels к приложению
app.include_router(router_rooms)
app.include_router(router_facilities)
app.include_router(router_bookings)


'''Создание первой основной ручки'''
@app.get("/")  # HTTP метод GET для получения данных
def func():
    return "Hello World!"


if __name__ == "__main__":  # Запуск приложения сервера через uvicorn
    uvicorn.run("main:app", reload=True)

