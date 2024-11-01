from aiogram.types import Message
from aiogram.filters import BaseFilter
from database.NisDB import NisDB

class IsUserInDB(BaseFilter):
    def __init__(self):
        self.db = NisDB()


    async def __call__(self, message: Message):
        return self.db.is_user_in_db(message.from_user.id)

