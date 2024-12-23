from aiogram.fsm.state import State, StatesGroup


class CurrentStates(StatesGroup):
    waiting_for_click = State()
    waiting_for_sum = State()
    waiting_for_purpose = State()
    waiting_for_category = State()
