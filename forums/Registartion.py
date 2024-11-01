from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

class RegistrationForum(StatesGroup):
    name = State()
    group = State()
class UpdateForum(StatesGroup):
    name = State()
    group = State()
    