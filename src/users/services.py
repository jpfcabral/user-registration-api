from src.users.models import User, UserDB
from src.users.repository import UserRepository

class UserService:
    def __init__(self) -> None:
        self.__user_repository = UserRepository()

    def create_user_db(self, user: User):
        user_db = UserDB.parse_obj(user)
        return self.__user_repository.insert(user_db.name, user_db.email, user_db.password, user_db.checked)

    def get_user_from_db(self, user_id: int):
        if not user_id:
            return self.__user_repository.read()
        return self.__user_repository.read_by_id(user_id)
