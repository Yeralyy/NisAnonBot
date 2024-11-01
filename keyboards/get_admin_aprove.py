from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


def get_admin_aprove_keyboard() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Done✅", callback_data="yeah"))
    builder.row(InlineKeyboardButton(text="Edit❌", callback_data="nuh"))
    builder.adjust(2)
    return builder.as_markup()
    
    