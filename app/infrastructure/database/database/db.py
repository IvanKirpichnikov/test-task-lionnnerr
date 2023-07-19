from psycopg import AsyncConnection

from app.infrastructure.database.database.data import _DataDB
from app.infrastructure.database.database.user import _UserDB


class DB:
    def __init__(self, connect: AsyncConnection) -> None:
        self.data = _DataDB(connect=connect)
        self.user = _UserDB(connect=connect)
