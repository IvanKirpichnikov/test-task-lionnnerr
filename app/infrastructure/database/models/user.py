from datetime import datetime as date_time

from app.abc.model import AbstractModel


class UserModel(AbstractModel):
    id: int
    tid: int
    cid: int
    datetime: date_time
    phone_number: str
    email: str
