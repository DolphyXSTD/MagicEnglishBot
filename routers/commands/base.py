from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

import database
from keyboards import admin_keyboard
from config import admin_id

router = Router(name=__name__)

@router.message(Command('start'))
async def start(message : Message):
    if message.from_user.id == int(admin_id):
        await message.answer(text='Hello admin', reply_markup=admin_keyboard)
    else:
        database.add_user(message.from_user.id)
        await message.answer(text="Hi. I'm magic english bot")

