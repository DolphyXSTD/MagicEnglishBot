from aiogram.fsm.state import StatesGroup, State

class Admin(StatesGroup):
    send_post = State()