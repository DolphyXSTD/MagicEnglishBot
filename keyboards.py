from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Сделать пост')]])

user_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Изменить уровень')]])