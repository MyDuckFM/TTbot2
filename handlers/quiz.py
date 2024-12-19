from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.database import get_quiz_index, get_user_score, update_quiz_index, update_user_score, save_quiz_result
from utils.keyboard import generate_options_keyboard, show_main_keyboard, hide_main_keyboard, show_final_score
import config
import json

router = Router()

with open(config.DICT_DATA, 'r', encoding='utf-8') as j:
    quiz_data = json.loads(j.read())

@router.callback_query(F.data == "right_answer")
async def right_answer(callback: types.CallbackQuery):
    await handle_answer(callback, True)

@router.callback_query(F.data == "wrong_answer")
async def wrong_answer(callback: types.CallbackQuery):
    await handle_answer(callback, False)

async def handle_answer(callback: types.CallbackQuery, is_correct: bool):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    current_question_index = await get_quiz_index(callback.from_user.id)
    current_score = await get_user_score(callback.from_user.id)

    if is_correct:
        await callback.message.answer("Верно!")
        current_score += 1
    else:
        correct_option = quiz_data[current_question_index]['correct_option']
        await callback.message.answer(f"Неправильно. Правильный ответ: {quiz_data[current_question_index]['options'][correct_option]}")

    current_question_index += 1
    await update_quiz_index(callback.from_user.id, current_question_index)
    await update_user_score(callback.from_user.id, current_score)

    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        await callback.message.answer("Это был последний вопрос. Квиз завершен!")
        await save_quiz_result(callback.from_user.id, current_score)
        await show_main_keyboard(callback.message)
        await show_final_score(callback.message, current_score)

async def get_question(message, user_id):
    current_question_index = await get_quiz_index(user_id)
    correct_index = quiz_data[current_question_index]['correct_option']
    opts = quiz_data[current_question_index]['options']
    kb = generate_options_keyboard(opts, opts[correct_index])
    await message.answer(f"{quiz_data[current_question_index]['question']}", reply_markup=kb)

async def new_quiz(message):
    user_id = message.from_user.id
    current_question_index = 0
    new_score = 0
    await update_quiz_index(user_id, current_question_index)
    await update_user_score(user_id, new_score)
    await get_question(message, user_id)
    await hide_main_keyboard(message)

@router.message(F.text == "Начать игру")
@router.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
    await message.answer(f"Давайте начнем квиз!")
    await new_quiz(message)
