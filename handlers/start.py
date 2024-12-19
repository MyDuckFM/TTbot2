from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from utils.keyboard import show_main_keyboard

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await show_main_keyboard(message)
