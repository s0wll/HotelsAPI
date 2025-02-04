from repositories.base import BaseRepository
from models.rooms import RoomsOrm



class RoomsRepository(BaseRepository):
    model = RoomsOrm