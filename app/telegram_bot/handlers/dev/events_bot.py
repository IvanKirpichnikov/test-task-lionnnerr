from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.filters import ChatMemberUpdatedFilter, MEMBER, KICKED
from aiogram.types import ChatMemberUpdated

from app.infrastructure.database.database.db import DB

router = Router()
router.my_chat_member.filter(F.chat.type == ChatType.PRIVATE.value)


@router.my_chat_member(ChatMemberUpdatedFilter(KICKED >> MEMBER))
async def new_user(event: ChatMemberUpdated, db: DB):
    tid = event.from_user.id

    await db.user.add(
        tid=tid,
        cid=event.chat.id
    )
    await db.data.add(tid=tid)


@router.my_chat_member(ChatMemberUpdatedFilter(MEMBER >> KICKED))
async def delete_user(event: ChatMemberUpdated, db: DB):
    await db.user.delete(tid=event.from_user.id)
