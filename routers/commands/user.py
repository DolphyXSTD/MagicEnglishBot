from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

import database

from states import User

ENGLISH_LEVELS = ['A1','A2','B1','B2','C1','C2']

router = Router(name=__name__)

@router.message(Command("level"))
@router.message(F.text == 'Изменить уровень')
async def set_level_start(message : Message, state : FSMContext):
    await state.set_state(User.set_level)
    await message.answer('Выбери свой уровень английского!')

@router.message(User.set_level)
async def set_level(message : Message, state : FSMContext):
    if message.text in ENGLISH_LEVELS:
        database.set_level(message.from_user.id, message.text)
        await state.clear()
        await message.answer('Твой уровень успешно обновлен!')
    else:
        await message.answer('Выбери уровень из вариантов: A1, A2, B1, B2, C1, C2.')