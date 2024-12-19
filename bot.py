import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters.command import Command
from aiogram import F
from handlers import start, quiz, help, stats
from utils.database import create_table
import config

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.API_TOKEN)
dp = Dispatcher()

async def main():
    await create_table()
    dp.include_router(start.router)
    dp.include_router(quiz.router)
    dp.include_router(help.router)
    dp.include_router(stats.router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
