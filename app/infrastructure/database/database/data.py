from logging import getLogger

from asyncpg import Connection

from app.infrastructure.database.database.base import BaseDB

logger = getLogger()


class _DataDB(BaseDB):
    table_name = 'data'
    
    def __init__(self, connect: Connection) -> None:
        self.connect = connect
    
    async def create_table(self) -> None:
        async with self.connect.transaction():
            await self.connect.execute('''
                CREATE TABLE IF NOT EXISTS data(
                    id int REFERENCES users ON DELETE CASCADE,
                    phone_number TEXT DEFAULT '',
                    email TEXT DEFAULT ''
                );
            ''')
            logger.info("Created table '%s'", self.table_name)
    
    async def add(self, *, tid: int) -> None:
        async with self.connect.transaction():
            await self.connect.execute('''
                INSERT INTO data(id)
                SELECT users.id FROM users
                WHERE users.tid = $1;
            ''', tid
            )
    
    async def update_email(self, *, tid: int, email: str) -> None:
        async with self.connect.transaction():
            await self.connect.execute('''
                UPDATE data SET email = $1
                FROM users WHERE users.id = data.id
                AND users.tid = $2;
            ''', email, tid
            )
            logger.info(
                "Update email. db='%s', tid='%d', email='%s'",
                self.table_name, tid, email
            )
    
    async def update_phone_number(
        self,
        *,
        tid: int,
        phone_number: str
    ) -> None:
        async with self.connect.transaction():
            await self.connect.execute('''
                UPDATE data SET phone_number = $1
                FROM users WHERE users.id = data.id
                AND users.tid = $2;
            ''', phone_number, tid
            )
            logger.info(
                "Update phone_number. db='%s', tid='%d', phone_number='%s'",
                self.table_name, tid, phone_number
            )
