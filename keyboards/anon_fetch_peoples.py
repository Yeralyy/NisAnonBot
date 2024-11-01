from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


def fetch_peoples(peoples: list) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    for people in peoples:
        builder.row(InlineKeyboardButton(text=people[0], callback_data=f"person_{people[0]}"))
    builder.row(InlineKeyboardButton(text="<<<", callback_data="back_to_the_grade"))
    if len(peoples) % 3 == 0:
        builder.adjust(3)
    elif len(peoples) % 4 == 0:
        builder.adjust(4)
    elif len(peoples) % 5 == 0:
        builder.adjust(5)
    return builder.as_markup()
    