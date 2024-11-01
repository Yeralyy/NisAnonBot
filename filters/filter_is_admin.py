from aiogram.types import Message
from aiogram.filters import BaseFilter
from database.NisDB import NisDB

class IsUserAdmin(BaseFilter):
    async def __call__(self, message: Message):
        db = NisDB()
        
        return db.is_user_admin(message.from_user.id)  
        
    