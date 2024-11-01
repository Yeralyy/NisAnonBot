from aiogram.types import Message, CallbackQuery

from aiogram import Router, F

from aiogram.fsm.context import FSMContext

import run


async def send_media_message(
        chat_id, 
        state_data, 
        caption,
        bot=run.bot,
        reply_markup=None):
    if state_data.get("photo") is not None:
        await bot.send_photo(chat_id=chat_id, photo=state_data["photo"], caption=caption, reply_markup=reply_markup)
    elif state_data.get("video") is not None:
        await bot.send_video(chat_id=chat_id, video=state_data["video"], caption=caption, reply_markup=reply_markup)
    else:
        await bot.send_message(chat_id=chat_id, text=caption, reply_markup=reply_markup)

