from aiogram.filters import BaseFilter
from typing import Union

from aiogram.types import Message

# Filter for chat type
class ChatTypeFIlter(BaseFilter):
    def __init__(self, chat_type: Union[str, list]):
        self.chat_type = chat_type


    async def __call__(self, message: Message):
        if isinstance(self.chat_type, str):
            return message.chat.type == self.chat_type
        else:
            return message.chat.type == self.chat_type    