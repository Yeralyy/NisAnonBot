from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


def get_paralell() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    for i in range(7, 13):
        builder.row(InlineKeyboardButton(text=f"{i}", callback_data=f"parallel_{i}"))
    builder.adjust(3)
    return builder.as_markup()
    

def get_class(parallel: int) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    grades = ""
    if parallel == 7:
        grades = "ABCDEFGHI"
    if parallel == 8:
        grades = "ABCDEFGHIJK"
    if parallel == 9 or parallel == 11:
        grades = "ABCDEFGHI"
    if parallel == 10 or parallel == 12:
        grades = "ABCDEF"    

    for letter in grades:
        builder.row(InlineKeyboardButton(text=letter, callback_data=f"san_{letter}"))
    builder.adjust(3)
    return builder.as_markup()    