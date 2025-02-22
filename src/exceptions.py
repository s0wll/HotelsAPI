class Booking_ServiceException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(Booking_ServiceException):
    detail = "Объект не найден"


class AllRoomsAreBookedException(Booking_ServiceException):
    detail = "Не осталось свободных номеров"