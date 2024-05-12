from aiogram.fsm.state import StatesGroup, State


class MainDialogSG(StatesGroup):
    start = State()
    get_role = State()
    dialog = State()