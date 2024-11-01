from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


def get_aprovee() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Done✅", callback_data="done"))
    builder.row(InlineKeyboardButton(text="Edit❌", callback_data="edit"))
    builder.adjust(2)
    return builder.as_markup()
    
    