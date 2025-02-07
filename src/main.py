from fastapi import FastAPI
import uvicorn

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.api.auth import router as router_auth  # Импорт роутера auth
from src.api.hotels import router as router_hotels  # Импорт роутера hotels
from src.api.rooms import router as router_rooms  # Импорт роутера rooms


app = FastAPI()  # Приложение - объект класса FastAPI

app.include_router(router_auth)
app.include_router(router_hotels)  # Подключение роутера hotels к приложению
app.include_router(router_rooms)


'''Создание первой основной ручки'''
@app.get("/")  # HTTP метод GET для получения данных
def func():
    return "Hello World!"


if __name__ == "__main__":  # Запуск приложения сервера через uvicorn
    uvicorn.run("main:app", reload=True)

