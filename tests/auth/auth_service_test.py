# pylint: disable=W0621:redefined-outer-name

from datetime import datetime, timedelta
import pytest
from fastapi import HTTPException
from freezegun import freeze_time
from src.auth.models import ValidationCode
from src.auth.services import AuthService
from src.users.models import User, UserDB

@pytest.fixture
def user_obj_helper():
    obj = User(name='Joao', email='jpfcabral@gmail.com', password='123456')
    return obj

@pytest.fixture
def user_db_checkedhelper():
    obj = UserDB(id=1, name='Joao', email='jpfcabral@gmail.com', password='123456', checked=True)
    return obj

@pytest.fixture
def user_db_checkedhelper_not_checked():
    obj = UserDB(id=1, name='Joao', email='jpfcabral@gmail.com', password='123456', checked=False)
    return obj


@pytest.fixture
def validation_code_helper():
    obj = ValidationCode(email='jpfcabral@gmail.com', code=4123, updated_at=datetime.now())
    return obj

def test_create_user_db(mocker, user_obj_helper):
    mocker.patch("src.users.repository.UserRepository.insert", return_value= UserDB.parse_obj(user_obj_helper))
    mocker.patch("src.users.repository.UserRepository.read_by_email", return_value= None)
    mocker.patch("src.auth.repository.AuthRepository.read", return_value= None)
    mocker.patch("src.auth.repository.AuthRepository.insert", return_value= None)

    user_db = AuthService().create_user(user_obj_helper)

    assert isinstance(user_db, UserDB)
    assert user_db.checked is False

def test_create_user_db_already_exist_error(mocker, user_obj_helper):
    with pytest.raises(HTTPException) as e_info:
        mocker.patch("src.users.repository.UserRepository.insert", return_value= UserDB.parse_obj(user_obj_helper))
        mocker.patch("src.users.repository.UserRepository.read_by_email", return_value= UserDB.parse_obj(user_obj_helper))
        mocker.patch("src.auth.repository.AuthRepository.read", return_value= None)
        mocker.patch("src.auth.repository.AuthRepository.insert", return_value= None)

        AuthService().create_user(user_obj_helper)

    assert e_info.type == HTTPException


def test_send_validation_code(mocker, user_obj_helper):
    mocker.patch("src.users.repository.UserRepository.insert", return_value= UserDB.parse_obj(user_obj_helper))
    mocker.patch("src.users.repository.UserRepository.read_by_email", return_value= None)
    mocker.patch("src.auth.repository.AuthRepository.read", return_value= None)
    mocker.patch("src.auth.repository.AuthRepository.insert", return_value= None)

    validation_code = AuthService().send_validation_code(user_obj_helper)

    assert isinstance(validation_code, ValidationCode)
    assert isinstance(validation_code.code, int)

def test_send_validation_code_already_checked(mocker, user_obj_helper, user_db_checkedhelper):
    with pytest.raises(HTTPException) as e_info:
        mocker.patch("src.users.repository.UserRepository.insert", return_value= UserDB.parse_obj(user_obj_helper))
        mocker.patch("src.users.repository.UserRepository.read_by_email", return_value= user_db_checkedhelper)
        mocker.patch("src.auth.repository.AuthRepository.read", return_value= validation_code_helper)
        mocker.patch("src.auth.repository.AuthRepository.insert", return_value= None)

        AuthService().send_validation_code(user_obj_helper)

    assert e_info.type == HTTPException

def test_validate_code(mocker, user_obj_helper, validation_code_helper, user_db_checkedhelper_not_checked):
    mocker.patch("src.users.repository.UserRepository.insert", return_value= UserDB.parse_obj(user_obj_helper))
    mocker.patch("src.users.repository.UserRepository.read_by_email", return_value= user_db_checkedhelper_not_checked)
    mocker.patch("src.auth.repository.AuthRepository.read", return_value= validation_code_helper)
    mocker.patch("src.auth.repository.AuthRepository.insert", return_value= None)

    AuthService().validate_code(user_obj_helper, code=4123)

def test_validate_code_error(mocker, user_obj_helper, validation_code_helper, user_db_checkedhelper_not_checked):
    with pytest.raises(HTTPException) as e_info:
        mocker.patch("src.users.repository.UserRepository.insert", return_value= UserDB.parse_obj(user_obj_helper))
        mocker.patch("src.users.repository.UserRepository.read_by_email", return_value= user_db_checkedhelper_not_checked)
        mocker.patch("src.auth.repository.AuthRepository.read", return_value= validation_code_helper)
        mocker.patch("src.auth.repository.AuthRepository.insert", return_value= None)

        AuthService().validate_code(user_obj_helper, code=1234)

    assert e_info.type == HTTPException

@freeze_time(datetime.now() + timedelta(seconds=80))
def test_validate_code_timeout(mocker, user_obj_helper, validation_code_helper, user_db_checkedhelper_not_checked):
    with pytest.raises(HTTPException) as e_info:
        mocker.patch("src.users.repository.UserRepository.insert", return_value= UserDB.parse_obj(user_obj_helper))
        mocker.patch("src.users.repository.UserRepository.read_by_email", return_value= user_db_checkedhelper_not_checked)
        mocker.patch("src.auth.repository.AuthRepository.read", return_value= validation_code_helper)
        mocker.patch("src.auth.repository.AuthRepository.insert", return_value= None)

        AuthService().validate_code(user_obj_helper, code=4123)

    assert e_info.type == HTTPException
