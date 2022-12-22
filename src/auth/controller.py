from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from fastapi import Depends
from src.auth.services import AuthService
from src.users.models import User, UserRead

router = InferringRouter(tags=['Auth'])
auth = AuthService()

@cbv(router)
class AuthController:
    def __init__(self) -> None:
        self.__auth_service = AuthService()

    @router.post('/register', response_model=UserRead)
    def create_user(self, user: User):
        return self.__auth_service.create_user(user=user)

    @router.get('/verify', response_model=UserRead)
    def verify_token(self, code: int, user: User = Depends(auth.authenticate)):
        return self.__auth_service.validate_code(user=user, code=code)

    @router.post('/verify')
    def update_validation_code(self, user: User = Depends(auth.authenticate)):
        self.__auth_service.send_validation_code(user)
        return {'status': 'Verify your mail box'}
