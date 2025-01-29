from fastapi import FastAPI, Query, Body
import uvicorn

app = FastAPI()  # Приложение - объект класса FastAPI



hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
]

'''Создание второй ручки hotels'''
@app.get("/hotels")
def get_hotels(
    id: int | None = Query(None, description="Айдишник"),  # id - параметр, который будет передаваться в URL, Query - декоратор, который позволяет указать описание параметра (название)
                                              # int | None - означает, что параметр необязателен к заполнению в FastAPI
    title: str | None = Query(None, description="Название отеля"),  # title - параметр, который будет передаваться в URL, Query - декоратор, который позволяет указать описание параметра (название)
                                              # str | None - означает, что параметр необязателен к заполнению в FastAPI
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_


'''Создание POST ручки на добавление отелей'''
# body, request body
@app.post("/hotels")
def create_hotel(
    title: str = Body(embed=True),  # title - параметр, который будет передаваться в теле запроса, Body - декоратор для передачи данных не через Query
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title
    })
    return {"status": "OK"}


'''Создание ручки удаления для /hotels'''
@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}

'''Создание первой основной ручки'''
@app.get("/")  # HTTP метод GET для получения данных
def func():
    return "Hello World!"

if __name__ == "__main__":  # Запуск приложения сервера через uvicorn
    uvicorn.run("main:app", reload=True)
