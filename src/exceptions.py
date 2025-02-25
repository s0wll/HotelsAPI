from datetime import date

from fastapi import HTTPException


class Booking_ServiceException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(Booking_ServiceException):
    detail = "Объект не найден"


class ObjectAlreadyExistsException(Booking_ServiceException):
    detail = "Похожий объект уже существует"


class AllRoomsAreBookedException(Booking_ServiceException):
    detail = "Не осталось свободных номеров"


def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_to <= date_from:
        raise HTTPException(status_code=400, detail="Дата заезда не может быть позже даты выезда")
    

class Booking_ServiceHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code = self.status_code, detail = self.detail)


class HotelNotFoundHTTPException(Booking_ServiceHTTPException):
    status_code = 404
    detail = "Отель не найден"


class RoomNotFoundHTTPException(Booking_ServiceHTTPException):
    status_code = 404
    detail = "Номер не найден"