from aiogram.types import Message, CallbackQuery
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest

from filters.chat_filter import ChatTypeFIlter
from filters.filter_is_admin import IsUserAdmin

from keyboards.get_audience import get_audience_keyboard
from keyboards.get_admin_aprove import get_admin_aprove_keyboard
from keyboards.add_admin_photo import add_photo
from keyboards.fetch_grades import fetch_grades_keyboard

from keyboards.main_funcktions import options_keyboard

from database.NisDB import NisDB
import asyncio
import run

from constants import CANCEL, ASKING_GROUP, ASKING_TEXT \
, ASKING_GRADE, USER_TEXT, ASKING_MEDIA, WRONG_FILE_TYPE, NEW_MESSAGE \
, MESSAGE_SUCCESSFULLY, NOT_ADMIN

from forums.NewsLetter import ForumNewsLetter

router = Router()


router.message.filter(ChatTypeFIlter("private"))




@router.message(IsUserAdmin(), F.text == "Public announcement🔊")
async def newsletter(message: Message, state: FSMContext):
    await state.clear()
    
    await state.update_data(pub=True)
    
    await message.answer(text=ASKING_GROUP, reply_markup=get_audience_keyboard())

@router.message(F.text == "Public announcement🔊")
async def newsletter(message: Message, state: FSMContext):
    await state.clear()
    
    await message.answer(text=NOT_ADMIN)
    



@router.callback_query(F.data == "send_all")
async def newsletter_send_all(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=ASKING_TEXT)
    await callback.answer()
    await state.set_state(ForumNewsLetter.asking_message_text)

@router.callback_query(F.data == "send_by_grades")
async def newsletter_send_by_grades(callback: CallbackQuery):
    db = NisDB()
    grades = db.get_grades()
    await callback.message.edit_text(text=ASKING_GRADE, reply_markup=fetch_grades_keyboard(grades))

@router.callback_query(F.data.startswith("grade_"))
async def get_message_for_grade(callback: CallbackQuery, state: FSMContext):
    await state.update_data(grade=callback.data)
    await callback.message.edit_text(text=ASKING_TEXT)
    await callback.answer()
    await state.set_state(ForumNewsLetter.asking_message_text)

@router.message(ForumNewsLetter.asking_message_text, F.text)
async def is_ready(message: Message, state: FSMContext):
    await state.update_data(content=message.html_text)
    await message.answer(text=USER_TEXT.format(message.html_text), reply_markup=add_photo())

@router.callback_query(F.data == "photo")
async def adding_photo(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=ASKING_MEDIA)
    await state.set_state(ForumNewsLetter.asking_message_media)

@router.callback_query(F.data == "move")
async def continue_process(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=USER_TEXT.format((await state.get_data())["content"]),
        reply_markup=get_admin_aprove_keyboard()
    )

    await state.set_state(ForumNewsLetter.asking_message_aprove)

@router.message(ForumNewsLetter.asking_message_media, F.photo)
async def handle_photo(message: Message, state: FSMContext):
    await state.update_data(photo=message.photo[-1].file_id)
    await message.answer_photo(
        photo=message.photo[-1].file_id,
        caption=USER_TEXT.format((await state.get_data())["content"]),
        reply_markup=get_admin_aprove_keyboard()
    )
    await state.set_state(ForumNewsLetter.asking_message_aprove)

@router.message(ForumNewsLetter.asking_message_media, F.video)
async def handle_video(message: Message, state: FSMContext):
    await state.update_data(video=message.video.file_id)
    await message.answer_video(
        video=message.video.file_id,
        caption=USER_TEXT.format((await state.get_data())["content"]),
        reply_markup=get_admin_aprove_keyboard()
    )
    await state.set_state(ForumNewsLetter.asking_message_aprove)

@router.message(ForumNewsLetter.asking_message_media)
async def not_media(message: Message):
    await message.answer(text=WRONG_FILE_TYPE)

@router.callback_query(ForumNewsLetter.asking_message_aprove, F.data == "yeah")
async def send_message(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    db = NisDB()
    users = db.fetchall_users() if (await state.get_data()).get("grade", None) is None else db.fetchall_grade_users(grade=(await state.get_data())["grade"].replace("grade_", ""))
    
    state_data = await state.get_data()

    async def send_message_to_user(user):
        user_id = int(user[0])
        try:
            if (await state.get_data()).get("photo", None) is not None:
                await run.bot.send_photo(chat_id=user_id, photo=(await state.get_data())["photo"], caption=NEW_MESSAGE.format(state_data["content"]))
            elif (await state.get_data()).get("video", None) is not None:
                await run.bot.send_video(chat_id=user_id, video=(await state.get_data())["video"], caption=NEW_MESSAGE.format(state_data["content"]))
            else:
                await run.bot.send_message(chat_id=user_id, text=NEW_MESSAGE.format(state_data["content"]))
            return 1
        except TelegramForbiddenError:
            print(f"[INFO] User {user_id} blocked the bot")
            return 0
        except Exception as e:
            print(f"[ERROR] Failed to send message to user {user_id}: {e}")
            return 0

    tasks = [send_message_to_user(user) for user in users]
    count = sum(await asyncio.gather(*tasks))

    print(f"[INFO] {count} users received the message")

    try:
        print(f"[INFO] {callback.from_user.id} sent message")
        await callback.message.answer(text=MESSAGE_SUCCESSFULLY)    
    except TelegramBadRequest:
        pass

    await state.clear()

@router.callback_query(ForumNewsLetter.asking_message_aprove, F.data == "nuh")
async def not_approved(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.edit_text(text=ASKING_TEXT)
    except TelegramBadRequest:
        pass
    await callback.answer()
    await state.set_state(ForumNewsLetter.asking_message_text)