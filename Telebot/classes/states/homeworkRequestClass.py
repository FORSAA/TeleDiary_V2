from aiogram.fsm.state import StatesGroup, State


class HomeworkRequest(StatesGroup):
    selecting_day = State()
    selecting_type = State()
    awaiting_answer = State()