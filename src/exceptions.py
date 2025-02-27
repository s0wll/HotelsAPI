from datetime import date

from fastapi import HTTPException


class Booking_ServiceException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(Booking_ServiceException):
    detail = "Объект не найден"


class RoomNotFoundException(ObjectNotFoundException):
    detail = "Номер не найден"


class HotelNotFoundException(ObjectNotFoundException):
    detail = "Отель не найден"


class UserNotFoundException(ObjectNotFoundException):
    detail = "Пользователь не найден"


class IncorrectPasswordException(Booking_ServiceException):
    detail = "Неверный пароль"


class ObjectAlreadyExistsException(Booking_ServiceException):
    detail = "Похожий объект уже существует"


class UserAlreadyExistsException(ObjectAlreadyExistsException):
    detail = "Пользователь уже существует"


class AllRoomsAreBookedException(Booking_ServiceException):
    detail = "Не осталось свободных номеров"


class IncorrectTokenException(Booking_ServiceException):
    detail = "Некорректный токен"


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


class AllRoomsAreBookedHTTPException(Booking_ServiceHTTPException):
    status_code = 409
    detail = "Не осталось свободных номеров"


class IncorrectTokenHTTPException(Booking_ServiceHTTPException):
    status_code = 401
    detail = "Некорректный токен"


class UserEmailAlreadyExistsHTTPException(Booking_ServiceHTTPException):
    status_code = 409
    detail = "Пользователь с такой почтой уже существует"


class UserEmailNotFoundException(Booking_ServiceHTTPException):
    status_code = 401
    detail = "Пользователь с такой почтой не найден"


class IncorrectPasswordHTTPException(Booking_ServiceHTTPException):
    status_code = 401
    detail = "Неверный пароль"


class NotAuthenticatedHTTPException(Booking_ServiceHTTPException):
    status_code = 401
    detail="Вы не аутентифицированны/Вы не предоставили токен доступа"