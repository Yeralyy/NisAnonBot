from aiogram.fsm.state import State, StatesGroup


class ForumNewsLetter(StatesGroup):
    asking_message_text = State()
    asking_message_media = State()
    asking_message_aprove = State()