from src.users.models import User, UserDB
from src.users.repository import UserRepository

class UserService:
    def __init__(self) -> None:
        self.__user_repository = UserRepository()

    def create_user_db(self, user: User):
        user_db = UserDB.parse_obj(user)
        return self.__user_repository.insert(user_db)

    def get_user_from_db(self, user: User):
        return self.__user_repository.read_by_email(user.email)
