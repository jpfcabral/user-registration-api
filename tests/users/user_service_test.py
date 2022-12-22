# pylint: disable=W0621:redefined-outer-name

import pytest
from src.users.models import User, UserDB
from src.users.services import UserService

@pytest.fixture
def user_obj_helper():
    obj = User(name='Joao', email='jpfcabral@gmail.com', password='123456')
    return obj

@pytest.fixture
def user_db_helper():
    obj = UserDB(id=1, name='Joao', email='jpfcabral@gmail.com', password='123456', checked=False)
    return obj

def test_get_user_from_db(mocker, user_obj_helper):
    mocker.patch("src.users.repository.UserRepository.read_by_email", return_value= UserDB.parse_obj(user_obj_helper))

    user_db = UserService().get_user_from_db(user_obj_helper)

    assert user_db.email == 'jpfcabral@gmail.com'
