from src.infra.database import DBConnectionHandler
from src.users.models import User, UserDB

class UserRepository:

    def insert(self, user: User):
        name = user.name
        email = user.email
        password = user.password
        checked = False

        with DBConnectionHandler() as database:
            try:
                query = '''insert into users (name, email, password, checked) values ('{}', '{}', '{}', {}) returning id'''
                database.cursor.execute(query.format(name, email, password, checked))
                database.connection.commit()

                user_id = database.cursor.fetchone()[0]
                return self.read_by_id(user_id)
            except:
                database.connection.rollback()
                raise

    def read(self):
        with DBConnectionHandler() as database:
            try:
                users = []
                query = '''select * from users'''
                database.cursor.execute(query)
                data = database.cursor.fetchall()

                for row in data:
                    users.append(UserDB(id=row[0], name=row[1], email=row[2], password=row[3], checked=row[4]))

                return users
            except:
                database.connection.rollback()
                raise

    def read_by_id(self, user_id: int):
        with DBConnectionHandler() as database:
            try:
                query = '''select * from users where id = {}'''
                database.cursor.execute(query.format(user_id))
                data = database.cursor.fetchone()
                return UserDB(id=data[0], name=data[1], email=data[2], password=data[3], checked=data[4])
            except:
                database.connection.rollback()
                raise

    def read_by_email(self, email: int):
        with DBConnectionHandler() as database:
            try:
                query = '''select * from users where email = %s'''
                database.cursor.execute(query, (email,))
                data = database.cursor.fetchone()

                if data:
                    return UserDB(id=data[0], name=data[1], email=data[2], password=data[3], checked=data[4])
                return None
            except:
                database.connection.rollback()
                raise

    def update_checked_status(self, user_id):
        with DBConnectionHandler() as database:
            try:
                query = '''update users set checked = TRUE where id = %s'''
                database.cursor.execute(query, (user_id,))
                database.connection.commit()

                return self.read_by_id(user_id=user_id)
            except:
                database.connection.rollback()
                raise
