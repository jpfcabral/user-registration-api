from typing import Optional
from pydantic import BaseModel # pylint: disable=E0611:no-name-in-module


class User(BaseModel):
    name: str
    email: str
    password: str

    def __rep__(self):
        return f"User [name={self.name}, email={self.email}"

class UserDB(User):
    id: Optional[int]
    checked: bool = False

    def __rep__(self):
        return f"User [name={self.name}, email={self.email}, checked={self.checked}]"


class UserRead(BaseModel):
    id: int
    name: str
    email: str
    checked: bool

    def __rep__(self):
        return f"User [name={self.name}, email={self.email}, checked={self.checked}]"
