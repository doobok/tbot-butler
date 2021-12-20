from aiogram import types

from utils.misc.menu_utils import menu_str


def main_menu():
    k = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    return k.row(
        types.KeyboardButton(text=menu_str['add-income']),
        types.KeyboardButton(text=menu_str['add-cost']),
    ).row(
        types.KeyboardButton(text=menu_str['projects']),
        types.KeyboardButton(text=menu_str['add-user']),
    )


def go_to_main():
    k = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    return k.add(types.KeyboardButton(text=menu_str['main-menu']))


def cancel_menu():
    k = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    return k.add(types.KeyboardButton(text=menu_str['cancel']))


def confirm_add_user():
    k = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    return k.row(
        types.KeyboardButton(text=menu_str['cancel']),
        types.KeyboardButton(text=menu_str['add-user-conf']),
    )
