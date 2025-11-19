from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Сделать пост')],
                                               [KeyboardButton(text='Редактировать базу данных')]])

edit_db_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Добавить текст')],
                                                 [KeyboardButton(text='Добавить слова')]])

user_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Изменить уровень')]])

english_level_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='A1'), KeyboardButton(text='A2')],
                                                       [KeyboardButton(text='B1'), KeyboardButton(text='B2')],
                                                       [KeyboardButton(text='C1'), KeyboardButton(text='C2')]])

yes_no_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Yes'),KeyboardButton(text='No')]])