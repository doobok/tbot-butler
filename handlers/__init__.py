from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart

from handlers.base import bot_start, add_user1, add_user2, bot_restart, add_user3, add_user4, external_menu, users_list
from handlers.category import category_list, category_list_select, add_cat1, add_cat2, category_create, category_remove
from handlers.cost import add_cost, pay_cat_select, sum_validate, \
    add_income, show_incomes, nav_pays, show_costs, delete_pay, pay_comment
from handlers.currency import opn_currency, select_currency, use_currency, menu_currency
from handlers.project import projects_list
from states.mane import UserAdd, CatEdit, PayAdd, PaysList, CurrencySection
from utils.callbacks.category_callback import cat_list_item, cat_item_global, confirm, remove, navigate
from utils.callbacks.currency_callback import currency_select
from utils.misc.menu_utils import menu_str


def setup(dp: Dispatcher):
    dp.register_message_handler(bot_start, CommandStart(), state="*")
    dp.register_message_handler(bot_restart, text=[menu_str['cancel'], menu_str['main-menu']], state="*")
    dp.register_message_handler(external_menu, text=[menu_str['ext-menu']], state="*")

    dp.register_message_handler(add_user1, text=[menu_str['add-user']], state="*")
    dp.register_message_handler(add_user2, content_types='contact', state=UserAdd.wait_for_contact)
    dp.register_message_handler(add_user3, state=UserAdd.wait_for_name)
    dp.register_message_handler(add_user4, text=[menu_str['add-user-conf']], state=UserAdd.wait_for_confirm)
    dp.register_message_handler(users_list, text=[menu_str['users']], state="*")

    dp.register_message_handler(category_list, text=[menu_str['cat-cost'], menu_str['cat-income']], state="*")
    dp.register_callback_query_handler(category_list_select, cat_list_item(None),
                                       state=(CatEdit.in_menu, CatEdit.wait_for_confirm))
    dp.register_message_handler(add_cat1, content_types='text', state=CatEdit.in_menu)
    dp.register_callback_query_handler(add_cat2, cat_item_global(None), state=CatEdit.wait_for_type)
    dp.register_callback_query_handler(category_create, confirm(None), state=CatEdit.wait_for_confirm)
    dp.register_callback_query_handler(category_remove, remove(None), state=CatEdit.in_menu)

    dp.register_message_handler(add_cost, text=[menu_str['add-cost']], state="*")
    dp.register_message_handler(add_income, text=[menu_str['add-income']], state="*")
    dp.register_message_handler(show_costs, commands=['costs'], state="*")
    dp.register_message_handler(show_costs, text=[menu_str['costs']], state="*")
    dp.register_message_handler(show_incomes, commands=['incomes'], state="*")
    dp.register_message_handler(show_incomes, text=[menu_str['incomes']], state="*")
    dp.register_callback_query_handler(pay_cat_select, cat_list_item(None), state=PayAdd.wait_for_cat)
    dp.register_message_handler(sum_validate, state=PayAdd.wait_for_cat)
    dp.register_message_handler(pay_comment, state=PayAdd.wait_for_comment)
    dp.register_callback_query_handler(nav_pays, navigate(None), state=PaysList.in_list)
    dp.register_message_handler(delete_pay, regexp_commands=['delpay_([0-9]*)'], state=PaysList.in_list)

    dp.register_message_handler(opn_currency, text=[menu_str['currency']], state="*")
    dp.register_message_handler(menu_currency, text=[menu_str['get-currency']], state=CurrencySection.in_currency)
    dp.register_callback_query_handler(select_currency, currency_select(None), state=CurrencySection.in_currency)
    dp.register_message_handler(use_currency, state=CurrencySection.in_currency)

    dp.register_message_handler(projects_list, text=[menu_str['projects']], state="*")

