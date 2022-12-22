import os
from dotenv import load_dotenv

load_dotenv('.env')

class Settings: # pylint: disable=R0903:too-few-public-methods
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'registration')

    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecretkey')

settings = Settings()
