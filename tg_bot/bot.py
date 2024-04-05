import asyncio
from aiogram import Bot
from aiogram import Dispatcher
from config import load_config
from data import processing_handlers
from handlers import chat_handlers


async def main() -> None:
    """
    Инициализация бота.
    :return:
    """
    config = load_config()
    bot: Bot = Bot(token=config.tg_bot.token)
    dp: Dispatcher = Dispatcher()
    dp.include_routers(chat_handlers.r, processing_handlers.r)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
