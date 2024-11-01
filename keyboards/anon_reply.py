from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def reply_keybaord(user_id: int) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="reply🤠", callback_data=f"reply_{user_id}"))
    builder.row(InlineKeyboardButton(text="ignore🙊", callback_data="ignor_message"))

    builder.adjust(2)
    return builder.as_markup()
    
    