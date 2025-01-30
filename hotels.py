from fastapi import Query, APIRouter, Body

from dependencies import PaginationDep
from schemas.hotels import Hotel, HotelPATCH


router = APIRouter(prefix="/hotels", tags=["Отели"])  # Концепция роутер для подключения ручек hotels к приложению




hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]

'''Создание второй ручки hotels'''
@router.get(
        "",
        summary="Получение отеля",
        description="Тут можно получить определенный отель или все отели",
)
def get_hotels(
    pagination: PaginationDep,
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

    if pagination.page and pagination.per_page:  # if page и per_page переданы
        return hotels_[pagination.per_page * (pagination.page - 1):][:pagination.per_page]  # Решение учителя
        #return hotels_[per_page * (page - 1):per_page * page] # Я решил так

    return hotels_


'''Создание POST ручки на добавление отелей'''
# body, request body
@router.post(
        "",
        summary="Добавление отеля",
        description="Тут можно добавить новый отель",
)
def create_hotel(hotel_data: Hotel = Body(openapi_examples={  # # Использование в качестве параметров атрибуты из класса Hotel
    "1": {"summary": "Сочи", "value": {
        "title": "Отель Сочи 5 звезд у моря",
        "name": "sochi_u_morya",
    }}, "2": {"summary": "Дубай", "value": {
        "title": "Отель Дубай у фонтана",
        "name": "dubai_fountain",
    }}, 
})
):  
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name,
    })
    return {"status": "OK"}


'''Создание PUT ручки для полного изменения отеля (кроме id)'''
@router.put(
        "/{hotel_id}",
        summary="Полное изменение отеля",
        description="Тут мы полностью обновляем данные об отеле",
)
def edit_hotel(
    hotel_id: int,  # Параметр пути Path() (т.к. в пути app.put мы указали hotel_id, то в параметрах основной функции это будет именно Path() параметр)
    hotel_data: Hotel,  # Использование в качестве параметров атрибуты из класса Hotel
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    hotel["title"] = hotel_data.title
    hotel["name"] = hotel_data.name
    return {"status": "OK"}


'''Создание PATCH ручки для частичного или полного изменения отеля'''
@router.patch(
        "/{hotel_id}",
        summary="Частичное обновление данных об отеле",
        description="Тут мы частично обновляем данные об отеле: можно отправить name, а можно title",
)
def partially_edit_hotel(
    hotel_id: int,
    hotel_data: HotelPATCH,
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if hotel_data.title:
        hotel["title"] = hotel_data.title
    if hotel_data.name:
        hotel["name"] = hotel_data.name
    return {"status": "OK"}


'''Создание ручки удаления для /hotels'''
@router.delete(
        "/{hotel_id}",
        summary="Удаление отеля",
        description="Тут можно удалить определенный отель",
)
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}