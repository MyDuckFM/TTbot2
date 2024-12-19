from aiogram import Router, types, F
from aiogram.filters import Command

router = Router()

@router.message(Command(commands="help"))
@router.message(F.text == "Помощь")
async def cmd_help(message: types.Message):
    await message.answer("Вы нажали на кнопку помощи!")
