from aiogram import Router, F

from aiogram.types import Message

from aiogram.fsm.context import FSMContext

from filters.is_user_in_db import IsUserInDB
from filters.chat_filter import ChatTypeFIlter 

from forums.MessageSend import ChatMessageForum

from constants import ASKING_TEXT

router = Router(name="inst_handler")

router.message.filter(
    ChatTypeFIlter("private")
)
router.message.filter(
    IsUserInDB()
)

@router.message(F.text == "Instagram📲")
async def get_text(
    message: Message,
    state: FSMContext
):

    await state.clear()
    await message.answer(text='<b>All anonymous <u>Instagram</u> messages - <a href="https://www.instagram.com/ship_uralsk?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw==">here</a></b>')
    await message.answer(text=ASKING_TEXT)


    await state.update_data(inst=True)
    await state.set_state(ChatMessageForum.text) 
    


