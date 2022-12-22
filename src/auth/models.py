from datetime import datetime
from pydantic import BaseModel # pylint: disable=E0611:no-name-in-module


class ValidationCode(BaseModel):
    email: str
    code: int
    updated_at: datetime

    def __rep__(self):
        return f"ValidationCode [email={self.email}, updated_at={self.updated_at}"
