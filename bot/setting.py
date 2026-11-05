import asyncio
import logging
from os import getenv
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.handlers import router

load_dotenv()
TOKEN = getenv("BOT_TOKEN")

async def main() -> None:
    logging.basicConfig(level=logging.INFO)          # в консоли видно, что происходит
    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),  # <b>жирный</b> по умолчанию
    )
    dp = Dispatcher()
    dp.include_router(router)                        # подключаем обработчики

    await bot.delete_webhook(drop_pending_updates=True)  # пропустить сообщения, пришедшие пока бот был выключен
    await dp.start_polling(bot)


# if __name__ == "__main__":
#     asyncio.run(main())