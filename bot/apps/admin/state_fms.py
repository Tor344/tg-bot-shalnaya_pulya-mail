from aiogram.fsm.state import State,StatesGroup

class Admin(StatesGroup):
    get_file = State()