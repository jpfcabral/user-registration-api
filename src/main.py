from fastapi import FastAPI
from src.users.controller import router as users_router
from src.auth.controller import router as auth_router
from src.infra.database import DBConnectionHandler

app = FastAPI()
database = DBConnectionHandler()

database.create_db_and_tables()
app.include_router(users_router, prefix='/users')
app.include_router(auth_router, prefix='/auth')
