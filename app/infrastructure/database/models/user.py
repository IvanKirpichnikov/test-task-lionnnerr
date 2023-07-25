from datetime import datetime as datetime
from dataclasses import dataclass
from typing import Optional

from app.infrastructure.database.models.base import BaseModel


@dataclass(frozen=True)
class UserDataModel(BaseModel):
    id: int
    tid: int
    cid: int
    username: Optional[str] = None
    datetime: datetime
    phone_number: str
    email: str

@dataclass(frozen=True)
class UserOrderModel(BaseModel):
    user_data: UserDataModel
    text: str
