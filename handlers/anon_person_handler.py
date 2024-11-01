from aiogram import Router, F

from aiogram.types import Message, CallbackQuery

from aiogram.fsm.context import FSMContext

from filters.is_user_in_db import IsUserInDB
from filters.chat_filter import ChatTypeFIlter 

from forums.MessageSend import ChatMessageForum

from database.NisDB import NisDB

from keyboards.anon_fetch_grades import fetch_grades_keyboard
from keyboards.anon_fetch_peoples import fetch_peoples
from keyboards.anon_question import questions_keyboard

from constants import ASK_GRADE, ASK_PERSON, ASKING_TEXT

router = Router(name="chat_handler")

router.message.filter(
    ChatTypeFIlter("private")
)
router.message.filter(
    IsUserInDB()
)

@router.message(F.text == "Person👤")
async def fetch_grades(
    message: Message,
    state: FSMContext
):
    await state.clear()

    db = NisDB()
    grades = db.get_grades()

    await message.answer(
        text=ASK_GRADE,
        reply_markup=fetch_grades_keyboard(grades=grades)
    )

@router.callback_query(F.data.startswith("group_"))
async def get_users_grade(
    callback: CallbackQuery, 
    state: FSMContext
):

    db = NisDB()
    peoples = db.get_peoples_by_grade(grade=callback.data.replace("group_", ""), user_id=callback.from_user.id)
    await callback.message.edit_text(text=ASK_PERSON, reply_markup=fetch_peoples(peoples=peoples))
    await callback.answer()

    await state.set_state(ChatMessageForum.people)


@router.callback_query(F.data == "back_to_the_grade")
async def back(callback: CallbackQuery):
    db = NisDB()
    await callback.message.edit_text(text=ASK_GRADE, reply_markup=fetch_grades_keyboard(db.get_grades()))

@router.callback_query(F.data.startswith("person_"))
async def send_message_person(callback: CallbackQuery, state: FSMContext):
    db = NisDB()
    person_id = db.get_person(callback.data.replace("person_", ""))
    await state.update_data(person_id=person_id[0][0])

    await callback.message.delete()
    await callback.message.answer(text=ASKING_TEXT + "\n\nOr chose the question to ask😸", reply_markup=questions_keyboard())

    await state.set_state(ChatMessageForum.text)
    await callback.answer()




