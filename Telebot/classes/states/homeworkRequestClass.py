from aiogram.fsm.state import StatesGroup, State


class HomeworkRequest(StatesGroup):
    selecting_day = State()
    selecting_wish_type = State()
