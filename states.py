from aiogram.fsm.state import StatesGroup, State

class Admin(StatesGroup):
    send_post = State()
    set_level = State()
    edit_db = State()
    add_text = State()
    add_word = State()
    continuing = State()

class User(StatesGroup):
    set_level = State()