from aiogram.fsm.state import State,StatesGroup

class Code(StatesGroup):
    set_mail_data = State()
    request = State()