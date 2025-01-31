from fastapi import FastAPI
import uvicorn

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.api.hotels import router as router_hotels  # Импорт роутера hotels


app = FastAPI()  # Приложение - объект класса FastAPI

app.include_router(router_hotels)  # Подключение роутера hotels к приложению


'''Создание первой основной ручки'''
@app.get("/")  # HTTP метод GET для получения данных
def func():
    return "Hello World!"


if __name__ == "__main__":  # Запуск приложения сервера через uvicorn
    uvicorn.run("main:app", reload=True)


# add new libraries sqlalchemy, alembic, asyncpg for working with database and connect database