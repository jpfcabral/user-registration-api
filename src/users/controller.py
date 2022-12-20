from typing import Optional
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from src.users.models import User
from src.users.services import UserService

router = InferringRouter(tags=['Users'])

@cbv(router)
class UserController:
    def __init__(self) -> None:
        self.__user_service = UserService()

    @router.post('/')
    def create_user(self, user: User):
        self.__user_service.create_user_db(user)

    @router.get('/')
    def get_users(self, user_id: Optional[int] = None):
        return self.__user_service.get_user_from_db(user_id)