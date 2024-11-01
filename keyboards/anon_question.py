from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def questions_keyboard() -> ReplyKeyboardMarkup:
    row = [[KeyboardButton(text="Have a partner?💃"), KeyboardButton(text="birthday?🎂")], [KeyboardButton(text="Have gf/bf?👩‍❤️‍👨")]]
    return ReplyKeyboardMarkup(keyboard=row, resize_keyboard=True, input_field_placeholder="choose question")
    

