from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart

from handlers.base import bot_start, add_user1, add_user2, bot_restart, add_user3, add_user4, external_menu
from handlers.category import category_list, category_list_select
from states.mane import UserAdd, CatEdit
from utils.callbacks.category_callback import cat_list_item
from utils.misc.menu_utils import menu_str


def setup(dp: Dispatcher):
    dp.register_message_handler(bot_start, CommandStart(), state="*")
    dp.register_message_handler(bot_restart, text=[menu_str['cancel'], menu_str['main-menu']], state="*")
    dp.register_message_handler(external_menu, text=[menu_str['ext-menu']], state="*")
    dp.register_message_handler(add_user1, text=[menu_str['add-user']], state="*")
    dp.register_message_handler(add_user2, content_types='contact', state=UserAdd.wait_for_contact)
    dp.register_message_handler(add_user3, state=UserAdd.wait_for_name)
    dp.register_message_handler(add_user4, text=[menu_str['add-user-conf']], state=UserAdd.wait_for_confirm)
    dp.register_message_handler(category_list, text=[menu_str['cat-cost'], menu_str['cat-income']], state="*")
    dp.register_callback_query_handler(category_list_select, cat_list_item(None), state=CatEdit.in_menu)

