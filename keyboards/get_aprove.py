from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


def get_aprove() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Done✅", callback_data="yes"))
    builder.row(InlineKeyboardButton(text="Edit❌", callback_data="no"))
    builder.adjust(2)
    return builder.as_markup()
    
    