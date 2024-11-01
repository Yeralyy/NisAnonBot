from aiogram import Router, F

from aiogram.types import Message

from aiogram.fsm.context import FSMContext

from filters.is_user_in_db import IsUserInDB
from filters.chat_filter import ChatTypeFIlter 

from forums.MessageSend import ChatMessageForum

from constants import ASKING_CONTENT


router = Router(name="chat_handler")

router.message.filter(
    ChatTypeFIlter("private")
)
router.message.filter(
    IsUserInDB()
)

@router.message(F.text == "Chat💭")
async def get_text(
    message: Message,
    state: FSMContext
):
    await state.clear()
    await message.answer(text='<b>All anonymous messages - <a href="https://t.me/+8n7UkhYQwN4wNjgy">here</a></b>')
    
    await message.answer(text=ASKING_CONTENT)
    
    await state.update_data(chat=True)
    await state.set_state(ChatMessageForum.text)
    


