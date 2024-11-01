from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


def get_audience_keyboard() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Everyone👤", callback_data="send_all"))
    builder.row(InlineKeyboardButton(text="Certain group👥", callback_data="send_by_grades"))
    builder.adjust(2)
    return builder.as_markup()
    