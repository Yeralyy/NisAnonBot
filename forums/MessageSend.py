from aiogram.fsm.state import State, StatesGroup

class ChatMessageForum(StatesGroup):
    text = State()
    media = State()
    people = State()