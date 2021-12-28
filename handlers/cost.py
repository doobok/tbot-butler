import locale
import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode

from states.mane import PayAdd, PaysList
from utils.db.categories import Category
from utils.db.pays import Pay
from utils.keyboards.category_kbd import categories_select, nex_step
from utils.keyboards.global_kbd import go_to_main, pagination_nav
from utils.keyboards.pays_kbd import incomes_keyboard, costs_keyboard


async def add_cost(msg: types.Message, state: FSMContext):
    await msg.answer(f'Ви знаходитесь в розділі *{msg.text}*', reply_markup=go_to_main())
    await PayAdd.wait_for_cat.set()
    await state.update_data(pay_cat_model='cost')
    cat = await Category.view_dir(external_id=msg.from_user.id, model='cost', parent_id=0)
    await msg.answer('_Перейдіть в категорію для якої потрібно внести витрату_',
                     reply_markup=categories_select(categories=cat, item=None))


async def add_income(msg: types.Message, state: FSMContext):
    await msg.answer(f'Ви знаходитесь в розділі *{msg.text}*', reply_markup=go_to_main())
    await PayAdd.wait_for_cat.set()
    await state.update_data(pay_cat_model='income')
    cat = await Category.view_dir(external_id=msg.from_user.id, model='income', parent_id=0)
    await msg.answer('_Перейдіть в категорію для якої потрібно внести дохід_',
                     reply_markup=categories_select(categories=cat, item=None))


async def pay_cat_select(query: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await query.answer()
    data = await state.get_data()
    pay_cat_model = data.get('pay_cat_model')
    cat_id = int(callback_data['id'])
    await state.update_data(pay_cat_id=cat_id)
    item = await Category.view(cat_id=cat_id)
    cat = await Category.view_dir(external_id=query.message.chat.id, model=pay_cat_model, parent_id=cat_id)
    if item:
        txt = 'Обрано категорію *\[ %s \]*\n\n' \
              '_введіть суму, або продовжуйте переміщатись між категоріями_' \
              % item.get('name')
    else:
        txt = '_Перейдіть в категорію для якої потрібно внести витрату_'
    await query.message.edit_text(txt)
    await query.message.edit_reply_markup(reply_markup=categories_select(categories=cat, item=item))


async def sum_validate(msg: types.Message, state: FSMContext):
    val = list(map(float, re.findall(r"""\d+ # one or more digits
                              (?: # followed by...
                                  \. # a decimal point 
                                  \d+ # and another set of one or more digits
                              )? # zero or one times""",
                                     msg.text,
                                     re.VERBOSE)))
    if len(val) < 1:
        await msg.answer('Будь\-ласка, введіть число')
    else:
        summa = val[0]
        await state.update_data(pay_sum=summa)
        await msg.answer(f'Бажаєте внести {summa} грн?\n\n'
                         f'<i>вітправте мені нову суму, якщо потрібно скоригувати</i>',
                         parse_mode=ParseMode.HTML, reply_markup=nex_step())


async def pay_comment(query: types.CallbackQuery, state: FSMContext):
    await query.answer()
    await PayAdd.next()
    txt = '_Якщо потрібно \- залиште коментар, або просто натисніть Продовжити\.\n' \
          'В обох випадках дані будуть відразу збережені_'
    await query.message.edit_text(txt)
    await query.message.edit_reply_markup(reply_markup=nex_step())


async def confirm_comment(msg: types.Message, state: FSMContext):
    comment = msg.text
    txt = await save_pay_to_db(state=state, comment=comment, uid=msg.chat.id)
    await msg.answer(txt)


async def confirm_query(query: types.CallbackQuery, state: FSMContext):
    await query.answer()
    txt = await save_pay_to_db(state=state, comment='', uid=query.from_user.id)
    await query.message.edit_text(txt)


async def save_pay_to_db(state: FSMContext, comment: str, uid: int):
    data = await state.get_data()
    txt = ''
    if data['pay_cat_model'] == 'cost':
        await Pay.create_cost(summ=data['pay_sum'], comment=comment, cat=data['pay_cat_id'], uid=uid)
        txt = '_Дані успішно внесені, переглянути усі витрати можна тут 👉 /costs_'
    elif data['pay_cat_model'] == 'income':
        await Pay.create_income(summ=data['pay_sum'], comment=comment, cat=data['pay_cat_id'], uid=uid)
        txt = '_Дані успішно внесені, переглянути усі надходження можна тут 👉 /incomes_'
    await state.reset_state()
    return txt


async def show_incomes(msg: types.Message, state: FSMContext):
    await PaysList.in_list.set()
    await state.update_data(list_model='incomes', list_shift=0)
    await msg.answer('Ось перелік Ваших надходжень', reply_markup=incomes_keyboard())
    incomes = await Pay.pays(start=0, end=10, model='incomes', uid=msg.chat.id)
    await msg.answer(await format_list(incomes), parse_mode=ParseMode.HTML,
                     reply_markup=pagination_nav(start=0, count=len(incomes)))


async def show_costs(msg: types.Message, state: FSMContext):
    await PaysList.in_list.set()
    await state.update_data(list_model='costs', list_shift=0)
    await msg.answer('Ось перелік Ваших витрат', reply_markup=costs_keyboard())
    costs = await Pay.pays(start=0, end=10, model='costs', uid=msg.chat.id)
    await msg.answer(await format_list(costs), parse_mode=ParseMode.HTML,
                     reply_markup=pagination_nav(start=0, count=len(costs)))


async def nav_pays(query: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await query.answer()
    data = await state.get_data()
    list_shift = data['list_shift']
    if int(callback_data['forward']) > 0:
        list_shift = list_shift + 10
    else:
        list_shift = list_shift - 10
        if list_shift < 0:
            list_shift = 0
    await state.update_data(list_shift=list_shift)
    items = await Pay.pays(start=list_shift, end=list_shift+10, model=data['list_model'], uid=query.from_user.id)
    await query.message.edit_text(await format_list(items), parse_mode=ParseMode.HTML)
    await query.message.edit_reply_markup(reply_markup=pagination_nav(start=list_shift, count=len(items)))


async def format_list(items: list):
    txt = ['Список операцій:\n']
    if len(items) > 0:
        locale.setlocale(locale.LC_ALL, 'uk_UA.UTF-8')
        for item in items:
            txt.append('👉 <b>%s</b> [ %s ] \n<i><u>%s</u>\n%s</i> ' %
                       (locale.currency(float(item.get('sum')), grouping=True), item.get('name'), item.get('time'),
                        item.get('comment')))
    else:
        txt.append('💁‍♂️ Нічого не знайдено')
    return '\n'.join(txt)
