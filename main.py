import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

load_dotenv()

token = os.getenv('BOT_TOKEN')
admin_id = os.getenv('ADMIN_ID')

dp = Dispatcher()
bot = Bot(token=token)

admin_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Сделать пост')]])

@dp.message(Command('start'))
async def start(message : Message):
    if message.from_user.id == admin_id:
        await message.answer(text='Hello admin', reply_markup=admin_keyboard)
    else:
        await message.answer(text="Hi. I'm magic english bot")

@dp.message(lambda m: m.text == 'Сделать пост')
async def create_post(message: Message):
    if message.from_user.id == admin_id:
        await message.answer("Следующее сообщение - ваш пост")

@dp.message()
async def user_redirect(message : Message):
    await message.answer('Wait for new words and texts')

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

asyncio.run(main())