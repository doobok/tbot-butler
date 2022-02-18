from aiogram import types

from utils.callbacks.currency_callback import currency_select
from utils.misc.currency_utils import currency
from utils.misc.menu_utils import menu_str


def currency_list():
    k = types.InlineKeyboardMarkup()
    for cu in currency.keys():
        k.insert(types.InlineKeyboardButton(currency[cu], callback_data=currency_select(cu)))
    return k


def currency_menu():
    k = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    return k.row(
        types.KeyboardButton(text=menu_str['get-currency']),
        types.KeyboardButton(text=menu_str['main-menu']),
    )
