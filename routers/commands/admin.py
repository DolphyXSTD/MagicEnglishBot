from aiogram import F, Router, types
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

import database
from config import admin_id, ENGLISH_LEVELS
from states import Admin
from keyboards import *

router = Router(name=__name__)

db_edit_list = {'Добавить текст' : (Admin.add_text,'Введите текст'),
                'Добавить слова' : (Admin.add_word, 'Введите слова в формате:\n word\n translation\n example\n')}


@router.message(F.text == 'Сделать пост', lambda msg : msg.from_user.id == int(admin_id), default_state)
async def send_button_handler(message : Message, state : FSMContext):
    await state.set_state(Admin.send_post)
    await message.answer('Следующее сообщение будет разослано всем пользователям', reply_markup=types.ReplyKeyboardRemove())

@router.message(Admin.send_post)
async def send_post(message : Message, state : FSMContext):
    try:
        for user in database.get_all_users():
            await message.bot.copy_message(
                chat_id=user[0],
                from_chat_id=message.chat.id,
                message_id=message.message_id
            )
        await state.clear()
    except Exception as e:
        await message.answer(f'Сообщение не удалось разослать, попробуйте еще раз: {e}')

@router.message(F.text == 'Редактировать базу данных', lambda msg : msg.from_user.id == int(admin_id), default_state)
async def edit_button_handler(message : Message, state : FSMContext):
    await state.set_state(Admin.set_level)
    await message.answer('Введите уровень для редактирования', reply_markup=english_level_keyboard)

@router.message(Admin.set_level)
async def set_level(message : Message, state : FSMContext):
    if message.text in ENGLISH_LEVELS:
        await state.set_state(Admin.edit_db)
        await state.update_data(english_level = message.text)
        await message.answer('Выберите одну из следующих опций', reply_markup=edit_db_keyboard)
    else:
        await message.answer('Выбери уровень из вариантов: A1, A2, B1, B2, C1, C2.')

@router.message(Admin.edit_db)
async def check_option(message : Message, state : FSMContext):
    if message.text in db_edit_list:
        await state.set_state(db_edit_list[message.text][0])
        await message.answer(db_edit_list[message.text][1], reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer('Выберите корректную опцию.')

@router.message(Admin.add_text)
async def add_text(message : Message, state : FSMContext):
    data = await state.get_data()
    english_level = data.get("english_level")
    database.add_text(english_level, message.text)
    await state.set_state(Admin.continuing)
    await message.answer('Текст успешно добавлен. Продолжить работать в контексте данного уровня?', reply_markup=yes_no_keyboard)

@router.message(Admin.add_word)
async def add_words(message : Message, state : FSMContext):
    data = await state.get_data()
    english_level = data.get("english_level")
    wordlist = message.text.split(sep = '\n')
    if len(wordlist) % 3 > 0:
        await message.answer('Вы ввели неправильное количество данных. Пожалуйста, повторите ввод.')
    else:
        for i in range(len(wordlist)//3):
            database.add_word(english_level, wordlist[3*i], wordlist[3*i+1], wordlist[3*i+2])
        await state.set_state(Admin.continuing)
        await message.answer('Cлова успешно добавлены. Продолжить работать в контексте данного уровня?', reply_markup=yes_no_keyboard)

@router.message(Admin.continuing)
async def continue_handler(message : Message, state : FSMContext):
    if (message.text == 'Yes') or (message.text == 'Да'):
        await state.set_state(Admin.edit_db)
        await message.answer('Отлично! Продолжаем.', reply_markup=edit_db_keyboard)
    elif (message.text == 'No') or (message.text == 'Нет'):
        await state.clear()
        await message.answer('Возвращаюсь в главное меню', reply_markup=admin_keyboard)
    else:
        await message.answer('Не понял вас, введите Yes/No.')