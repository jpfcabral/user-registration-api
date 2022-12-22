from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from fastapi import Depends
from src.auth.services import AuthService
from src.users.models import User, UserRead
from src.users.services import UserService

router = InferringRouter(tags=['Users'])
auth = AuthService()

@cbv(router)
class UserController:
    def __init__(self) -> None:
        self.__user_service = UserService()

    @router.get('/me', response_model=UserRead) # pylint: disable=E1131:unsupported-binary-operation
    def get_users(self, user: User = Depends(auth.authenticate)):
        return self.__user_service.get_user_from_db(user)
