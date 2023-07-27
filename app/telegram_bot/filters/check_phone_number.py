from typing import Union, Literal

from aiogram.filters import BaseFilter
from aiogram.enums import MessageEntityType
from aiogram.types import Message


class CheckPhoneNumber(BaseFilter):
    async def __call__(
        self, message: Message
    ) -> Union[dict[str, str], Literal[False]]:
        contact = message.contact
        
        if contact:
            phone_number = contact.phone_number
            return dict(phone_number=phone_number)
        
        entities = message.entities
        
        data = {
            'phone_number': item.extract_from(message.text)
            for item in entities
            if item.type == MessageEntityType.PHONE_NUMBER.value
        }
        if data == {}:
            return False
        return data
