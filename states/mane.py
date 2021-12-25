from aiogram.dispatcher.filters.state import StatesGroup, State


class UserAdd(StatesGroup):
    wait_for_contact = State()
    wait_for_name = State()
    wait_for_confirm = State()


class CatEdit(StatesGroup):
    in_menu = State()
    wait_for_type = State()
    wait_for_confirm = State()


class PayAdd(StatesGroup):
    wait_for_cat = State()
    wait_for_comment = State()
