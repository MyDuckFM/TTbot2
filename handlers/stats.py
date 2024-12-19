from aiogram import Router, types, F
from aiogram.filters import Command
from utils.database import get_user_stats
import logging

router = Router()

@router.message(Command(commands="stats"))
@router.message(F.text.lower() == "статистика")
async def cmd_stats(message: types.Message):
    logging.info(f"Received stats command from user {message.from_user.id}")
    stats = await get_user_stats()
    stats_message = "\n".join([f"User ID: {user_id}, Score: {score}" for user_id, score in stats])
    await message.answer(f"Статистика игроков:\n{stats_message}")
