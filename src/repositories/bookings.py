from src.repositories.base import BaseRepository
from src.models.bookings import BookingsOrm
from repositories.mappers.mappers import BookingDataMapper



class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper