from repositories.base import BaseRepository
from models.users import UsersOrm
from schemas.users import User



class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = User