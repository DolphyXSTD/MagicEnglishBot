from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

import database
from config import admin_id
from states import Admin

router = Router(name=__name__)

@router.message(F.text == 'Сделать пост', lambda msg : msg.from_user.id == int(admin_id))
async def send_button_handler(message : Message, state : FSMContext):
    await state.set_state(Admin.send_post)
    await message.answer('Следующее сообщение будет разослано всем пользователям')

@router.message(Admin.send_post)
async def send_post(message : Message, state : FSMContext):
    try:
        for user in database.get_all_users():
            await message.bot.copy_message(
                chat_id=user,
                from_chat_id=message.chat.id,
                message_id=message.message_id
            )
        await state.clear()
    except Exception as e:
        await message.answer(f'Сообщение не удалось разослать, попробуйте еще раз: {e}')


