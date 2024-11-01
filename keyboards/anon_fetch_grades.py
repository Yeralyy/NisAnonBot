from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


def fetch_grades_keyboard(grades: list) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    for grade in grades:
        builder.row(InlineKeyboardButton(text=grade[0], callback_data=f"group_{grade[0]}"))

    builder.adjust(5)
    return builder.as_markup()
    