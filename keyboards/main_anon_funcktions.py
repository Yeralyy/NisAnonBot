from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def anon_options_keyboard() -> ReplyKeyboardMarkup:
    row = [
        [KeyboardButton(text="Chat💭"),
        KeyboardButton(text="Person👤")],
        [KeyboardButton(text="Instagram📲"), KeyboardButton(text="Back⬅️")]
    ]
    return ReplyKeyboardMarkup(keyboard=row, resize_keyboard=True, input_field_placeholder="choose options")