from src.repositories.mappers.base import DataMapper
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel


class HotelDataMapper(DataMapper):
    db_model = HotelsOrm
    schema = Hotel
