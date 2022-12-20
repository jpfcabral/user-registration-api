

class UserModel:
    id: int
    name: str
    email: str
    password: str
    checked: bool

    def __rep__(self):
        return f"User [name={self.name}, email={self.email}, checked={self.checked}]"
