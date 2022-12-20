import psycopg2
from psycopg2 import Error

from src.config import settings

class DBConnectionHandler:

    def __init__(self) -> None:
        self.connection = None
        self.cursor = None

    def __create_engine(self):
        return psycopg2.connect(
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            database=settings.DB_NAME
        )

    def create_db_and_tables(self):
        try:
            self.connection = self.__create_engine()
            self.cursor = self.connection.cursor()

            create_table_query = '''CREATE TABLE IF NOT EXISTS users
            (
                ID SERIAL PRIMARY KEY NOT NULL,
                NAME TEXT NOT NULL,
                EMAIL TEXT NOT NULL,
                PASSWORD TEXT NOT NULL,
                CHECKED BOOL NOT NULL
            )
            '''

            self.cursor.execute(create_table_query)
            self.connection.commit()
        except (Exception, Error) as error: # pylint: disable=W0703:broad-except
            print("Error while connecting to PostgreSQL", error)
        finally:
            if self.connection:
                self.cursor.close()
                self.connection.close()

    def __enter__(self):
        self.connection = self.__create_engine()
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.connection.close()
