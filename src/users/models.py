from typing import Optional
from pydantic import BaseModel # pylint: disable=E0611:no-name-in-module

class User(BaseModel):
    id: Optional[int]
    name: str
    email: str
    password: str
    checked: bool = False

    def __rep__(self):
        return f"User [name={self.name}, email={self.email}, checked={self.checked}]"

class UserCreate: # pylint: disable=R0903:too-few-public-methods
    name: str
    email: str
    password: str
