from aiogram import Router, F

from aiogram.types import Message

from aiogram.fsm.context import FSMContext

from filters.is_user_in_db import IsUserInDB
from filters.chat_filter import ChatTypeFIlter 

from aiogram.filters import CommandStart, Command

from keyboards.main_anon_funcktions import anon_options_keyboard

from keyboards.main_funcktions import options_keyboard

from constants import WELCOME_REG_MESSAGE, CHOSE_ANON_OPTIONS, CANCEL

router = Router()

router.message.filter(
    ChatTypeFIlter("private")
)
router.message.filter(
    IsUserInDB()
)

@router.message(CommandStart())
async def welcom(
    message: Message
):
    await message.answer(text=WELCOME_REG_MESSAGE.format(message.from_user.first_name), reply_markup=options_keyboard())



# options handlers

@router.message(Command("cancel"))
async def stop(message: Message, state: FSMContext):
    await message.answer(text=CANCEL, reply_markup=options_keyboard())
    await state.clear()

@router.message(F.text == "Anonymous messages🤫")
async def get_text(
    message: Message,
    state: FSMContext
):
    await state.clear()

    await message.answer(text=CHOSE_ANON_OPTIONS, reply_markup=anon_options_keyboard())


@router.message(F.text == "NIS🌱")
async def NIS(
    message: Message,
    state: FSMContext
):
    await state.clear()

    await message.answer(text='<b>Nazarbayev Intellectual Schools (NIS)</b> in Kazakhstan were established in <b>2011</b> 🎓 to enhance education, focusing on <b>STEM</b> (science, technology, engineering, and mathematics) 🔬💻. Instruction is <b>multilingual</b>, featuring Kazakh, Russian, and English 🌍. Admission is <b>competitive</b>, with students selected through entrance exams ✍️. Teachers engage in <b>ongoing professional development</b> 📈, ensuring modern teaching methods. NIS also emphasizes <b>extracurricular activities</b> 🎉, fostering personal growth alongside academic achievement. With several locations across the country 🏙️, NIS plays a crucial role in shaping future leaders in Kazakhstan.')

@router.message(F.text == "Back⬅️")
async def back(
    message: Message,
    state: FSMContext
)    :
    await state.clear()

    await message.answer(text="<b>Chose one of the main funcktions⤵️</b>", reply_markup=options_keyboard())
# @router.message(F.text == "to the someone")
# async def get_text(
#     message: Message,
#     state: FSMContext
# ):
#     pass
# @router.message(F.text == "to the instagram")
# async def get_text(
#     message: Message,
#     state: FSMContext
# ):
#     pass