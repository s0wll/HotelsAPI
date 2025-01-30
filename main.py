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


'''Создание PUT ручки для полного изменения отеля (кроме id)'''
@app.put("/hotels/{hotel_id}")
def edit_hotel(
    hotel_id: int,
    title: str = Body(embed=True, description="Новое название"),
    name: str =  Body(embed=True, description="Новое имя"),
):
    global hotels
    new_title = title
    new_name = name
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotels[hotel_id - 1]["title"] = new_title
            hotels[hotel_id - 1]["name"] = new_name
    return hotels[hotel_id - 1]


'''Создание PATCH ручки для частичного или полного изменения отеля'''
@app.patch("/hotels/{hotel_id}")
def update_hotel_partly(
    hotel_id: int,
    title: str | None = Query(None, description="Новое название"),
    name: str | None = Query(None, description="Новое имя"),
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id and title != None and name == None:
            hotels[hotel_id - 1]["title"] = title
            name = hotels[hotel_id - 1]["name"]
        elif hotel["id"] == hotel_id and name != None and title == None:
            hotels[hotel_id - 1]["name"] = name
            title = hotels[hotel_id - 1]["title"]
        elif hotel["id"] == hotel_id and name != None and title != None:
            hotels[hotel_id - 1]["title"] = title
            hotels[hotel_id - 1]["name"] = name 
        return hotels[hotel_id - 1]


'''Создание первой основной ручки'''
@app.get("/")  # HTTP метод GET для получения данных
def func():
    return "Hello World!"


if __name__ == "__main__":  # Запуск приложения сервера через uvicorn
    uvicorn.run("main:app", reload=True)
