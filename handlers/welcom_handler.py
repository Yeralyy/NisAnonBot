from aiogram import Router, F

from aiogram.types import Message, CallbackQuery

from aiogram.fsm.state import State
from aiogram.fsm.context import FSMContext

from filters.chat_filter import ChatTypeFIlter

from keyboards.main_funcktions import options_keyboard
from keyboards.get_group import get_class, get_paralell
from keyboards.reg_aprove import get_aprovee

from aiogram.filters import Command, CommandStart, StateFilter

from constants import WELCOM_MESSAGE, REGISTRATION_INSTRUCTION, POST_REGISTRATION_CONFIRMATION \
, WRONG_NAME_FORMAT, ASK_GRADE, ASK_PARALLEL, REGISTRATION_ERROR, CANCEL

from forums.Registartion import RegistrationForum 

from database.NisDB import NisDB

import re

router = Router()

router.message.filter(
    ChatTypeFIlter("private")
)



@router.message(Command("cancel"))
async def stop(message: Message, state: FSMContext):
    await message.answer(text=CANCEL)
    await state.clear()


# /start
@router.message(CommandStart())
async def start_cmd(
    message: Message,
    state: FSMContext):
    await message.answer(text=WELCOM_MESSAGE)
    await message.reply(text=REGISTRATION_INSTRUCTION)
    
    await state.set_state(RegistrationForum.name) 


# get user name
@router.message(F.text.regexp(re.compile(r'^[A-Z][a-z]+\s[A-Z]$')), RegistrationForum.name)
async def get_name(
    message: Message,
    state: FSMContext
):
    await message.answer(text=ASK_PARALLEL, reply_markup=get_paralell())
    
    await state.update_data(name=message.text)
    await state.set_state(RegistrationForum.group)

@router.message(StateFilter("RegistrationForum.name"))
async def wrong_name(messages: Message):
    await messages.answer(text=WRONG_NAME_FORMAT) 


@router.callback_query(F.data.startswith("parallel_"), RegistrationForum.group)
async def get_parallel(
    callback: CallbackQuery,
    state: FSMContext
):
    await state.update_data(parallel=int(callback.data.replace("parallel_", "")))

    await callback.message.edit_text(text=ASK_GRADE, reply_markup=get_class(int(callback.data.replace("parallel_", ""))))
    await callback.answer()



@router.callback_query(F.data.startswith("san_"))
async def get_reg_aprove(
    callback: CallbackQuery,
    state: FSMContext
):
    await state.update_data(synyp=callback.data.replace("san_", ""))

    data = await state.get_data()
    await callback.message.edit_text(
        text=f"Name: {data["name"]}\nparallel: {data["parallel"]}\ngrade: {data["synyp"]}",
        reply_markup=get_aprovee()
    )

    await callback.answer()



# get user group
@router.callback_query(F.data == "done")
async def save(
    callback: CallbackQuery,
    state: FSMContext
):
    db = NisDB()
    data = await state.get_data()

    result = db.save_data(
        user_id=callback.from_user.id,
        name=data["name"],
        parallel=data["parallel"],
        group=f"{data["parallel"]}{data["synyp"]}"
    )
    if result:
        await callback.message.delete()
        await callback.message.answer(text=POST_REGISTRATION_CONFIRMATION, reply_markup=options_keyboard())
        
        await state.clear()
    else:
        await callback.message.edit_text(text=REGISTRATION_ERROR)
        await state.set_state(RegistrationForum.name)
    
    await callback.answer()

@router.callback_query(F.data == "edit")
async def restart(
    callback: CallbackQuery,
    state: FSMContext
):
    await callback.message.edit_text(
        text="Ok, let's try again"
    )
    await callback.message.answer(text="<b>Enter your name\nusing the format mentioned above</b>")

    await state.set_state(RegistrationForum.name)
    await callback.answer()