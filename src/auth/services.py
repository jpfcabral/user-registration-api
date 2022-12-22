from datetime import datetime, timedelta
from random import randint
from fastapi import HTTPException, status
from fastapi import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from src.auth.models import ValidationCode
from src.auth.repository import AuthRepository
from src.users.models import User
from src.users.repository import UserRepository

security = HTTPBasic()


class AuthService:
    def __init__(self) -> None:
        self.__user_repository = UserRepository()
        self.__auth_repository = AuthRepository()

    def authenticate(self, credentials: HTTPBasicCredentials = Depends(security)):
        try:
            email = credentials.username
            password = credentials.password

            user = self.__user_repository.read_by_email(email)

            assert user.password == password
            return user
        except:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Crededentials') # pylint: disable=W0707:raise-missing-from

    def create_user(self, user: User):

        if self.__user_repository.read_by_email(user.email) is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email already used')
        try:
            user = self.__user_repository.insert(user=user)
            self.send_validation_code(user)

            return user
        except:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Error sending verification code') # pylint: disable=W0707:raise-missing-from

    def send_validation_code(self, user: User):

        if self._user_checked(user):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User already checked')

        code = randint(1000, 9999)
        validation_code = ValidationCode(email=user.email, code=code, updated_at=datetime.now())

        if self.__auth_repository.read(user.email):
            self.__auth_repository.update_code(user=user, code=code)
        else:
            self.__auth_repository.insert(validation_code)
        print(code)
        # body = {'email': user.email, 'code': code}
        # requests.post('http://thirdpartservice.com', json=body, timeout=5)

    def validate_code(self, user: User, code: int):
        if self._user_checked(user):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='User already checked')

        validation_code = self.__auth_repository.read(user.email)

        if datetime.now() - validation_code.updated_at > timedelta(seconds=60):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Expired code')

        if validation_code.code == code:
            user_db = self.__user_repository.read_by_email(user.email)
            return self.__user_repository.update_checked_status(user_db.id)

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid code')

    def _user_checked(self, user):
        user = self.__user_repository.read_by_email(user.email)
        return user.checked
