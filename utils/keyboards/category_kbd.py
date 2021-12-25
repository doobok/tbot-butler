from aiogram import types

from utils.callbacks.category_callback import cat_list_item, cat_item_global, confirm, remove
from utils.misc.menu_utils import menu_str


def categories_list(categories, item):
    k = types.InlineKeyboardMarkup()
    if len(categories) > 0:
        for cat in categories:
            k.insert(types.InlineKeyboardButton(cat['name'], callback_data=cat_list_item(cat['id'])))
    else:
        if item['global'] == 0:
            k.add(types.InlineKeyboardButton(menu_str['del'], callback_data=remove(item['id'])))
    if item:
        k.insert(types.InlineKeyboardButton(menu_str['back'], callback_data=cat_list_item(item['parent_id'])))
    return k


def select_cat_type():
    k = types.InlineKeyboardMarkup()
    return k.row(
        types.InlineKeyboardButton(menu_str['global'], callback_data=cat_item_global(1)),
        types.InlineKeyboardButton(menu_str['personal'], callback_data=cat_item_global(0)),
    )


def confirm_new_cat():
    k = types.InlineKeyboardMarkup()
    return k.row(
        types.InlineKeyboardButton(menu_str['go-to-root'], callback_data=cat_list_item(0)),
        types.InlineKeyboardButton(menu_str['confirm'], callback_data=confirm(True)),
    )


def go_to_root():
    k = types.InlineKeyboardMarkup()
    return k.row(
        types.InlineKeyboardButton(menu_str['go-to-root'], callback_data=cat_list_item(0)),
    )


def categories_select(categories, item):
    k = types.InlineKeyboardMarkup()
    if len(categories) > 0:
        for cat in categories:
            k.insert(types.InlineKeyboardButton(cat['name'], callback_data=cat_list_item(cat['id'])))
    if item:
        k.insert(types.InlineKeyboardButton(menu_str['back'], callback_data=cat_list_item(item['parent_id'])))
    return k


def nex_step():
    k = types.InlineKeyboardMarkup()
    return k.row(types.InlineKeyboardButton(menu_str['confirm'], callback_data=confirm(True)))
