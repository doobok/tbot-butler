from aiogram.dispatcher.filters.state import StatesGroup, State


class UserAdd(StatesGroup):
    wait_for_contact = State()
    wait_for_name = State()
    wait_for_confirm = State()
