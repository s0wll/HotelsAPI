from fastapi import FastAPI
import uvicorn

app = FastAPI()  # Приложение - объект класса FastAPI



hotels = [
    {"id": 1, "title": "Sochi"},
    {"id": 2, "title": "Дубай"},
]

'''Создание второй ручки hotels'''
@app.get("/hotels")
def get_hotels():
    return hotels


'''Создание первой основной ручки'''
@app.get("/")  # HTTP метод GET для получения данных
def func():
    return "Hello World!"

if __name__ == "__main__":  # Запуск приложения сервера через uvicorn
    uvicorn.run("main:app", reload=True)
