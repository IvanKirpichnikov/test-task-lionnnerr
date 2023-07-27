from dataclasses import dataclass
from typing import Optional

from app.infrastructure.database.models.base import BaseModel


@dataclass()
class UserDataModel(BaseModel):
    id: int
    tid: int
    cid: int
    datetime: str
    phone_number: str
    email: str
    username: Optional[str] = None

@dataclass()
class UserOrderModel(BaseModel):
    user_data: UserDataModel
    text: str
