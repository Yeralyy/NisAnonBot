from aiogram import Dispatcher
import asyncio
import CONFIG
import logging


from aiogram.fsm.storage.redis import RedisStorage

from handlers import welcom_handler, typical_handler, anon_chat_handler, anon_inst_handler, anon_person_handler, anon_sender \
, for_admin_handler


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(asctime)s - %(name)s - %(message)s"
)


storage = RedisStorage.from_url("redis://127.0.0.1:6379")

dp = Dispatcher(storage=storage)
bot = CONFIG.bot



async def main():

    dp.include_router(typical_handler.router)
    dp.include_router(anon_chat_handler.router)
    dp.include_router(anon_inst_handler.router)
    dp.include_router(anon_person_handler.router)
    dp.include_router(anon_sender.router)
    dp.include_router(for_admin_handler.router)

    dp.include_router(welcom_handler.router)

    await dp.start_polling(bot)



if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Keyboard interrupt")


