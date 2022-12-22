from src.users.models import User
from src.users.repository import UserRepository

class UserService:
    def __init__(self, user_repository: UserRepository = UserRepository()) -> None:
        self.__user_repository = user_repository

    def get_user_from_db(self, user: User):
        return self.__user_repository.read_by_email(user.email)
