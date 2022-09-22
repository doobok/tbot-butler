from aiogram import types

from data.config import admin
from utils.callbacks.category_callback import navigate
from utils.misc.menu_utils import menu_str


def main_menu():
    k = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    return k.row(
        types.KeyboardButton(text=menu_str['add-income']),
        types.KeyboardButton(text=menu_str['add-cost']),
    ).row(
        types.KeyboardButton(text=menu_str['projects']),
        types.KeyboardButton(text=menu_str['currency']),
        types.KeyboardButton(text=menu_str['ext-menu']),
    )


def ext_menu(uid: int):
    k = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    k.row(
        types.KeyboardButton(text=menu_str['incomes']),
        types.KeyboardButton(text=menu_str['costs']),
    ).row(
        types.KeyboardButton(text=menu_str['cat-income']),
        types.KeyboardButton(text=menu_str['cat-cost']),
    ).row(
        # types.KeyboardButton(text=menu_str['limits']),
        # types.KeyboardButton(text=menu_str['add-user']),
    )
    if uid == int(admin):
        k.row(
            types.KeyboardButton(text=menu_str['users']),
            types.KeyboardButton(text=menu_str['add-user']),
        )
    return k.add(types.KeyboardButton(text=menu_str['main-menu']))


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


def pagination_nav(start: int, count: int):
    k = types.InlineKeyboardMarkup()
    if start > 0:
        k.insert(types.InlineKeyboardButton(menu_str['back'], callback_data=navigate(0)))
    if count > 9:
        k.insert(types.InlineKeyboardButton(menu_str['forward'], callback_data=navigate(1)))
    return k
