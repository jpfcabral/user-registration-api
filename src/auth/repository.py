from datetime import datetime
from src.infra.database import DBConnectionHandler
from src.auth.models import ValidationCode
from src.users.models import User

class AuthRepository:
    def __init__(self) -> None:
        pass

    def insert(self, valid_model: ValidationCode):
        with DBConnectionHandler() as database:
            try:
                email = valid_model.email
                code = valid_model.code
                updated_at = valid_model.updated_at

                query = '''insert into codes (email, code, updated_at) values ('{}', '{}', '{}')'''
                database.cursor.execute(query.format(email, code, updated_at))
                database.connection.commit()
            except:
                database.connection.rollback()
                raise

    def read(self, email):
        with DBConnectionHandler() as database:
            try:
                query = '''select * from codes where email = %s'''
                database.cursor.execute(query, (email,))
                data = database.cursor.fetchone()
                if data:
                    return ValidationCode(email=data[0], code=data[1], updated_at=data[2])
                return None
            except:
                database.connection.rollback()
                raise

    def update_code(self, user: User, code: int):
        email = user.email
        time_now = datetime.now()

        with DBConnectionHandler() as database:
            try:
                query = '''update codes set code=%s, updated_at=%s where email=%s'''
                database.cursor.execute(query, (code, time_now, email))
                database.connection.commit()
                return None
            except:
                database.connection.rollback()
                raise
