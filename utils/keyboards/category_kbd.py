from aiogram import types

from utils.callbacks.category_callback import cat_list_item, del_cat_item
from utils.misc.menu_utils import menu_str


def categories_menu():
    k = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    return k.row(
        types.KeyboardButton(text=menu_str['add-cat']),
        types.KeyboardButton(text=menu_str['main-menu']),
    )


def categories_list(categories, item):
    k = types.InlineKeyboardMarkup()
    if len(categories) > 0:
        for cat in categories:
            k.insert(types.InlineKeyboardButton(cat['name'], callback_data=cat_list_item(cat['id'])))
    else:
        k.add(types.InlineKeyboardButton(menu_str['del'], callback_data=del_cat_item(item['id'])))
    if item:
        k.insert(types.InlineKeyboardButton(menu_str['back'], callback_data=cat_list_item(item['parent_id'])))
    return k
