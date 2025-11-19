from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import database
from keyboards import admin_keyboard, user_keyboard
from config import admin_id

router = Router(name=__name__)
@router.message(Command('id'))
async def get_id(message:Message):
    await message.answer(str(message.from_user.id))

@router.message(Command('start'))
async def start(message : Message, state :FSMContext):
    await state.clear()
    if message.from_user.id == int(admin_id):
        await message.answer(text='Hello admin', reply_markup=admin_keyboard)
    else:
        database.add_user(message.from_user.id)
        level = database.get_level(message.from_user.id)
        await message.answer(text=f"Hi. I'm magic english bot. Твой текущий уровень английского - {level}."
                                  f" Ты всегда можешь поменять его при помощи команды '/level'.", reply_markup=user_keyboard)

@router.message(Command('cancel'))
async def cancel(message : Message, state : FSMContext):

    if message.from_user.id == int(admin_id):
        await message.answer(text='Мы вернулись в главное меню', reply_markup=admin_keyboard)
    else:
        if state is not None:
            await message.answer(text='Действие отменено', reply_markup=types.ReplyKeyboardRemove())
    await state.clear()
