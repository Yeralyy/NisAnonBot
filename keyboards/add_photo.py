from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


def add_photo() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="add mediafile📸", callback_data="add_photo"))
    builder.row(InlineKeyboardButton(text="continue▶️", callback_data="continue"))
    builder.adjust(1)
    return builder.as_markup()
