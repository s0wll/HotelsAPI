# API ручки для /hotels(endpoints)
from datetime import date
from fastapi import APIRouter, Body, Query
from fastapi_cache.decorator import cache

# from src.database import engine  # Импорт объекта класса из файла database.py для Дебага запросов
from src.services.hotels import HotelsService
from src.exceptions import HotelNotFoundHTTPException, ObjectNotFoundException
from src.api.dependencies import PaginationDep, DBDep
from src.schemas.hotels import HotelAdd, HotelPATCH


router = APIRouter(
    prefix="/hotels", tags=["Отели"]
)  # Концепция роутер для подключения ручек hotels к приложению


"""Создание второй ручки hotels на получение отелей"""


@router.get(
    "",
    summary="Получение отеля",
    description="Тут можно получить определенный отель или все отели",
)
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,  # Параметры для пагинации
    db: DBDep,
    title: str | None = Query(
        None, description="Название отеля"
    ),  # title - параметр, который будет передаваться в URL, Query - декоратор, который позволяет указать описание параметра (название)
    # str | None - означает, что параметр необязателен к заполнению в FastAPI
    location: str | None = Query(None, description="Локация"),
    date_from: date = Query(example="2025-02-07"),
    date_to: date = Query(example="2025-02-09"),
):
    return await HotelsService(db).get_filtered_by_time(
        pagination,
        title,
        location,
        date_from,
        date_to,
    )
    

"""Ручка на получение одного отеля"""
@router.get("/{hotel_id}")
@cache(expire=10)
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        return await HotelsService(db).get_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


"""Создание POST ручки на добавление отелей"""
@router.post(
    "",
    summary="Добавление отеля",
    description="Тут можно добавить новый отель",
)
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={  # # Использование в качестве параметров атрибуты из класса Hotel
            "1": {
                "summary": "Сочи",
                "value": {
                    "title": "Отель Elite Resort 5 звезд у моря",
                    "location": "Сочи, ул. Моря, 1",
                },
            },
            "2": {
                "summary": "Дубай",
                "value": {
                    "title": "Отель Sheikh Resort у фонтана",
                    "location": "Дубай, ул. Шейха, 2",
                },
            },
        }
    ),
):
    hotel = await HotelsService(db).add_hotel(hotel_data)
    # print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))  # Вывод SQL запроса в консоль для дебага (делается только на этапе разработки для себя)
    return {"status": "OK", "data": hotel}


"""Создание PUT ручки для полного изменения отеля (кроме id)"""
@router.put(
    "/{hotel_id}",
    summary="Полное изменение отеля",
    description="Тут мы полностью обновляем данные об отеле",
)
async def edit_hotel(
    hotel_id: int,  # Параметр пути Path() (т.к. в пути app.put мы указали hotel_id, то в параметрах основной функции это будет именно Path() параметр)
    hotel_data: HotelAdd,  # Использование в качестве параметров атрибуты из класса Hotel
    db: DBDep,
):
    await HotelsService(db).edit_hotel(hotel_id, hotel_data)
    return {"status": "OK"}


"""Создание PATCH ручки для частичного или полного изменения отеля"""


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="Тут мы частично обновляем данные об отеле: можно отправить name, а можно title",
)
async def partially_edit_hotel(
    hotel_id: int,
    hotel_data: HotelPATCH,
    db: DBDep,
):
    await HotelsService(db).partially_edit_hotel(hotel_id, hotel_data)
    return {"status": "OK"}


"""Создание ручки удаления для /hotels"""


@router.delete(
    "/{hotel_id}",
    summary="Удаление отеля",
    description="Тут можно удалить определенный отель",
)
async def delete_hotel(hotel_id: int, db: DBDep):
    await HotelsService(db).delete_hotel(hotel_id)
    return {"status": "OK"}
