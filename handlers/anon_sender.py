from aiogram import Router, F

from aiogram.types import Message, CallbackQuery

from aiogram.fsm.context import FSMContext

from filters.is_user_in_db import IsUserInDB
from filters.chat_filter import ChatTypeFIlter 

from aiogram.filters import Command

from forums.MessageSend import ChatMessageForum

from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError

from keyboards.add_photo import add_photo
from keyboards.get_aprove import get_aprove
from keyboards.main_anon_funcktions import anon_options_keyboard
from keyboards.anon_reply import reply_keybaord

from utils import send_media_message

import run


from constants import USER_TEXT, WRONG_FILE_TYPE \
, MESSAGE_SUCCESSFULLY, ASKING_MEDIA, NEW_VALENTINE, NEW_ANON_REPLY, NEW_ANON_MESSAGE \
, USER_BLOCKED_BOT, ASKING_TEXT, IGNORED, NEW_ANON_STICKER, NEW_ANON_REPLY_STICKER \
, NEW_VALENTINE_STICKER, NEW_ANON_QUESTION, ASK_DICT

router = Router(name="anon_sender")

router.message.filter(
    ChatTypeFIlter("private")
)
router.message.filter(
    IsUserInDB()
)

@router.message(F.text.in_(["Have a partner?💃",  "birthday?🎂", "Have gf/bf?👩‍❤️‍👨"]), ChatMessageForum.text)
async def send_message(message: Message, state: FSMContext):

    state_data = await state.get_data()

    if state_data.get("content", None) is None:
        asking_question = message.text

        person_id = state_data["person_id"]

        
        await send_media_message(bot=run.bot, chat_id=person_id, state_data=state_data, caption=NEW_ANON_QUESTION + ASK_DICT[asking_question], reply_markup=reply_keybaord(user_id=message.from_user.id))
        

        


    await message.answer(text=MESSAGE_SUCCESSFULLY  + "\n\n<b>wait the answer!</b>", reply_markup=anon_options_keyboard())

    await state.clear()

@router.message(F.text, ChatMessageForum.text)
async def get_text(
    message: Message,
    state: FSMContext
):
    await state.update_data(content=message.html_text)

    await message.answer(text=USER_TEXT.format(message.html_text), reply_markup=add_photo())

# Фото немесе видео қосу
@router.callback_query(F.data == "add_photo")
async def adding_photo(callback: CallbackQuery, state: FSMContext):
    
    await callback.message.edit_text(text=ASKING_MEDIA)
    await state.set_state(ChatMessageForum.media)

# Мазмұнды мақұлдау
@router.callback_query(F.data == "continue")
async def contin(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.edit_text(text=USER_TEXT.format((await state.get_data()).get("content")), reply_markup=get_aprove())
    except TelegramBadRequest:
        print("Message edit erorr in anon sender, continue callback")


@router.message(ChatMessageForum.text, F.audio)
async def send_audio(message: Message, state: FSMContext):
    state_data = await state.get_data()


    if state_data.get("person_id") is None and state_data.get("messaged_person_id") is None:
        await run.bot.send_audio(chat_id=-1002228245987, audio=message.audio.file_id)
        print("[INFO] someone sent music to the chat")
        
    else:
        if state_data.get("messaged_person_id") is None:
            print("[INFO] someone sent music to the someone")

            await run.bot.send_message(chat_id=state_data["person_id"], text="<b>You have anonymous music🫣</b>")
            await run.bot.send_audio(chat_id=state_data["person_id"], audio=message.audio.file_id)
        else:
            print("[INFO] someone sent replyed music to the someone")

            await run.bot.send_message(chat_id=state_data["messaged_person_id"], text="<b>You have anonymous reply-music🫣</b>")
            await run.bot.send_audio(chat_id=state_data["messaged_person_id"], audio=message.audio.file_id, reply_markup=reply_keybaord(message.from_user.id))


    await message.answer(text=MESSAGE_SUCCESSFULLY, reply_markup=anon_options_keyboard())

    await state.clear()


# Стикер жіберу
@router.message(ChatMessageForum.text, F.sticker)
async def send_sticker(message: Message, state: FSMContext):
    state_data = await state.get_data()

    to_channel = False

    if state_data.get("inst") is True:
        print("[INFO] someone sent sticker to the instagram")
        await run.bot.send_message(chat_id=1196096873, text=NEW_VALENTINE_STICKER)
        await run.bot.send_sticker(chat_id=1196096873, sticker=message.sticker.file_id)
    else:
        if state_data.get("person_id") is None and state_data.get("messaged_person_id") is None:
            # await run.bot.send_sticker(chat_id=-1002228245987, sticker=message.sticker.file_id)
            to_channel = True
        else:
            if state_data.get("messaged_person_id") is None:
                print(f"[INFO] someone sent sticker to the someone")

                await run.bot.send_message(chat_id=state_data["person_id"], text=NEW_ANON_STICKER)
                await run.bot.send_sticker(chat_id=state_data["person_id"], sticker=message.sticker.file_id, reply_markup=reply_keybaord(message.from_user.id))

            else:

                print(f"[INFO] someone sent replyed sticker to the someone")
                
                await run.bot.send_message(chat_id=state_data["messaged_person_id"], text=NEW_ANON_REPLY_STICKER)
                await run.bot.send_sticker(chat_id=state_data["messaged_person_id"], sticker=message.sticker.file_id, reply_markup=reply_keybaord(message.from_user.id))

    if to_channel:
        await message.reply(text="<b>Only Text! Try again</b>")
    else:   
        await state.clear()
        await message.answer(text="sucesfully sended", reply_markup=anon_options_keyboard())


@router.message(ChatMessageForum.media, F.photo)
async def photo(message: Message, state: FSMContext):
    await state.update_data(photo=message.photo[-1].file_id)
    print(message.photo[-1].file_id)
    await message.answer_photo(photo=message.photo[-1].file_id, caption=(await state.get_data())["content"], reply_markup=get_aprove())


@router.message(ChatMessageForum.media, F.video)
async def video(message: Message, state: FSMContext):
    await state.update_data(video=message.video.file_id)
    await message.answer_video(
        video=message.video.file_id, 
        caption=(await state.get_data())["content"], 
        reply_markup=get_aprove()
        )


# Дұрыс файл түрі емес
@router.message(ChatMessageForum.media)
async def not_media(message: Message):
    await message.answer(text=WRONG_FILE_TYPE)


@router.callback_query(F.data == "yes")
async def send_message(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()


    if state_data.get("inst") is not None:
        print("[INFO] someone sent message to the instagram")

        await send_media_message(chat_id=1196096873, state_data=state_data, caption=NEW_VALENTINE.format(state_data["content"]))
        await send_media_message(chat_id=5686783384, state_data=state_data, caption=NEW_VALENTINE.format(state_data["content"]))
    else:
        
        if state_data.get("person_id", None) is None and state_data.get("messaged_person_id", None) is None:
            print("[INFO] someone sent message to the chat")

            await send_media_message(chat_id=-1002228245987, state_data=state_data, caption=state_data["content"])
        else:
            try:
                
                if state_data.get("messaged_person_id", None) is not None:
                    to_answer_person_id = state_data["messaged_person_id"]

                    print("[INFO] someone replyed message to the someone")

                    await send_media_message(chat_id=to_answer_person_id, state_data=state_data, caption=f"{NEW_ANON_REPLY}\n\n<tg-spoiler>{state_data['content']}</tg-spoiler>", reply_markup=reply_keybaord(user_id=callback.from_user.id))

                else:
                    person_id = state_data["person_id"]

                    print("[INFO] someone sent message to the someone")

                    await send_media_message(chat_id=person_id, state_data=state_data, caption=f"{NEW_ANON_MESSAGE}\n\n<tg-spoiler>{state_data['content']}</tg-spoiler>", reply_markup=reply_keybaord(user_id=callback.from_user.id))
            except TelegramForbiddenError:
                await callback.message.delete()
                await callback.message.answer(text=USER_BLOCKED_BOT, reply_markup=anon_options_keyboard())

    await callback.message.delete()
    await callback.message.answer(text=MESSAGE_SUCCESSFULLY, reply_markup=anon_options_keyboard())

    await state.clear()

    await callback.answer()




# Хабарламаға жауап беру
@router.callback_query(F.data.startswith("reply_"))
async def answer_back(callback: CallbackQuery, state: FSMContext):
    # print("[INFO] someon want to reply")
    await callback.message.answer(text=ASKING_TEXT)

    await state.update_data(messaged_person_id=int(callback.data.replace("reply_", "")))
    await state.set_state(ChatMessageForum.text)
    await callback.answer()



# Хабарламаны елемеу
@router.callback_query(F.data.startswith("ignor_"))
async def ignor(callback: CallbackQuery, state: FSMContext):
    
    print("[INFO] user ignored message")


    await callback.message.delete()
    await callback.message.answer(text=IGNORED)

    await state.clear()
    await callback.answer()

# Хабарламаны өңдеу
@router.callback_query(F.data == "no")
async def edit_message(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=ASKING_TEXT)
    await state.set_state(ChatMessageForum.text)
    await callback.answer()



@router.message(Command("cancel"))
async def cancel(
    message: Message,
    state: FSMContext
):
    await state.clear()
    await message.answer(text="Cancelled", reply_markup=anon_options_keyboard())
    