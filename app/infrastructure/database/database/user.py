from logging import getLogger

from asyncpg import Connection

from app.abc.database import AbstractDB
from app.infrastructure.database.models.user import UserModel


logger = getLogger(__name__)


class _UserDB(AbstractDB):
    table_name = 'users'
    
    def __init__(self, connect: Connection) -> None:
        super().__init__(connect)
        self.connect = connect
    
    async def create_table(self) -> None:
        async with self.connect.transaction():
            await self.connect.execute('''
                CREATE TABLE IF NOT EXISTS users(
                    id SERIAL PRIMARY KEY,
                    tid BIGINT UNIQUE,
                    cid BIGINT UNIQUE,
                    datetime TIMESTAMP DEFAULT now()
                );
            ''')
            logger.info("Created table '%s'", self.table_name)
    
    async def add_data(self, *, tid: int, cid: int) -> None:
        async with self.connect.transaction():
            await self.connect.execute('''
                INSERT INTO users(tid, cid, datetime)
                VALUES($1, $2) ON CONFLICT DO NOTHING;
            ''', tid, cid
            )
            logger.info(
                "Add user. db='%s', tid='%d', cid='%d'",
                self.table_name, tid, cid
            )
    
    async def delete_data(self, *, tid: int) -> None:
        async with self.connect.transaction():
            await self.connect.execute('''
                DELETE FROM users WHERE tid = $1;
            ''', tid
            )
            logger.info(
                "Delete user. db='%s', tid='%d'",
                self.table_name, tid
            )
    
    async def get_data(self, *, tid: int) -> UserModel:
        async with self.connect.transaction():
            cursor = await self.connect.cursor('''
                SELECT users.id,
                       users.tid,
                       users.cid,
                       users.datetime,
                       data.phone_number,
                       data.email
                FROM users, data
                WHERE users.tid = $1
            ''', tid
            )
            data = await cursor.fetchrow()
            return UserModel(**data)
