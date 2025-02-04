from repositories.base import BaseRepository
from models.hotels import HotelsOrm


class HotelsRepository(BaseRepository):
    model = HotelsOrm