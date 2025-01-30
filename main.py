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


'''Создание PUT ручки для полного изменения отеля (кроме id)'''
@app.put("/hotels/{hotel_id}")
def edit_hotel(
    hotel_id: int,  # Параметр пути Path() (т.к. в пути app.put мы указали hotel_id, то в параметрах основной функции это будет именно Path() параметр)
    title: str = Body(),
    name: str =  Body(),
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    hotel["title"] = title
    hotel["name"] = name
    return {"status": "OK"}


'''Создание PATCH ручки для частичного или полного изменения отеля'''
@app.patch("/hotels/{hotel_id}")
def partially_edit_hotel(
    hotel_id: int,
    title: str | None = Body(None),
    name: str | None = Body(None),
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if title:
        hotel["title"] = title
    if name:
        hotel["name"] = name
    return {"status": "OK"}

# git commit -m "fix: improve code for PUT and PATCH endpoints"


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
