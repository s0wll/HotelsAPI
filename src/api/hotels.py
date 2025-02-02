from fastapi import Query, APIRouter, Body

from sqlalchemy import insert, select
from sqlalchemy.sql.operators import like_op


# from src.database import engine  # Импорт объекта класса из файла database.py для Дебага запросов
from models.hotels import HotelsOrm
from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.schemas.hotels import Hotel, HotelPATCH


router = APIRouter(prefix="/hotels", tags=["Отели"])  # Концепция роутер для подключения ручек hotels к приложению


'''Создание второй ручки hotels на получение отелей'''
@router.get(
        "",
        summary="Получение отеля",
        description="Тут можно получить определенный отель или все отели",
)
async def get_hotels(
        pagination: PaginationDep,  # Параметры для пагинации
        title: str | None = Query(None, description="Название отеля"),  # title - параметр, который будет передаваться в URL, Query - декоратор, который позволяет указать описание параметра (название)
                                              # str | None - означает, что параметр необязателен к заполнению в FastAPI
        location: str | None = Query(None, description="Адрес отеля"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        query = select(HotelsOrm)  # stmt (statement - выражение) используется для всего кроме select, т.к. select - запрос на выборку данных, который возвращает результат, поэтому нужно называть query 
        if title:
            # query = query.filter(like_op(HotelsOrm.title, '{title}%'))  
            query = query.filter(HotelsOrm.title.contains(title))
        if location:
            # query = query.filter(like_op(HotelsOrm.location, '{title}%'))
            query = query.filter(HotelsOrm.location.contains(location))
        query = (
            query
            .limit(per_page)
            .offset(per_page * (pagination.page - 1))  # все что выше (с if и дальше) - пагинация с опциональной фильтрацией
        )
            
         # stmt (statement - выражение) используется для всего кроме select, т.к. select - запрос на выборку данных, который возвращает результат, поэтому нужно называть query
        result = await session.execute(query)

        hotels = result.scalars().all()
        # print(type(hotels), hotels)  # Принт в консоль для дебага (или можно в database.py у объекта engine приписать параметр echo=True)
        return hotels
        # commit() не нужно вызывать в select, т.к. commit() нужно вызывать когда мы хотим внести изменения в БД и зафиксировать это


'''Создание POST ручки на добавление отелей'''
@router.post(
        "",
        summary="Добавление отеля",
        description="Тут можно добавить новый отель",
)
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={  # # Использование в качестве параметров атрибуты из класса Hotel
    "1": {"summary": "Сочи", "value": {
        "title": "Отель Elite Resort 5 звезд у моря",
        "location": "Сочи, ул. Моря, 1",
    }}, "2": {"summary": "Дубай", "value": {
        "title": "Отель Sheikh Resort у фонтана",
        "location": "Дубай, ул. Шейха, 2",
    }}, 
})
):  
    async with async_session_maker() as session:  # Сессия (транзакция в БД) для отправления запроса в БД
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        # print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))  # Вывод SQL запроса в консоль для дебага (делается только на этапе разработки для себя)
        await session.execute(add_hotel_stmt)
        await session.commit()  # commit() нужно вызывать когда мы хотим внести изменения в БД и зафиксировать это

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