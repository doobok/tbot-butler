from aiogram import types

from utils.misc.menu_utils import menu_str


def costs_keyboard():
    k = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    return k.row(
        types.KeyboardButton(text=menu_str['main-menu']),
        types.KeyboardButton(text=menu_str['add-cost']),
    )


def incomes_keyboard():
    k = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    return k.row(
        types.KeyboardButton(text=menu_str['add-income']),
        types.KeyboardButton(text=menu_str['main-menu']),
    )