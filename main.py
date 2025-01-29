from fastapi import FastAPI, Query
import uvicorn

app = FastAPI()  # Приложение - объект класса FastAPI



hotels = [
    {"id": 1, "title": "Sochi"},
    {"id": 2, "title": "Дубай"},
]

'''Создание второй ручки hotels'''
@app.get("/hotels")
def get_hotels(
    id: int,  # id - параметр, который будет передаваться в URL

    title: str,  # title - параметр, который будет передаваться в URL
):
    return [hotel for hotel in hotels if hotel["title"] == title and hotel["id"] == id]  # Возврщение списка отфильтрованных hotel


'''Создание первой основной ручки'''
@app.get("/")  # HTTP метод GET для получения данных
def func():
    return "Hello World!"

if __name__ == "__main__":  # Запуск приложения сервера через uvicorn
    uvicorn.run("main:app", reload=True)
