from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.state import default_state
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

import database

from states import User
from config import ENGLISH_LEVELS
from keyboards import english_level_keyboard
router = Router(name=__name__)

@router.message(Command("level"), default_state)
@router.message(F.text == 'Изменить уровень', default_state)
async def set_level_start(message : Message, state : FSMContext):
    await state.set_state(User.set_level)
    await message.answer('Выбери свой уровень английского!', reply_markup=english_level_keyboard)

@router.message(User.set_level)
async def set_level(message : Message, state : FSMContext):
    if message.text in ENGLISH_LEVELS:
        database.set_level(message.from_user.id, message.text)
        await state.clear()
        await message.answer('Твой уровень успешно обновлен!', reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer('Выбери уровень из вариантов: A1, A2, B1, B2, C1, C2.')