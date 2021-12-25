import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode

from states.mane import PayAdd
from utils.db.categories import Category
from utils.db.pays import Pay
from utils.keyboards.category_kbd import categories_select, nex_step
from utils.keyboards.global_kbd import go_to_main


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
    txt = await save_pay_to_db(msg, state, comment)
    await msg.answer(txt)


async def confirm_query(query: types.CallbackQuery, state: FSMContext):
    await query.answer()
    comment = ''
    txt = await save_pay_to_db(query.message, state, comment)
    await query.message.edit_text(txt)


async def save_pay_to_db(msg: types.Message, state: FSMContext, comment: str):
    data = await state.get_data()
    txt = ''
    if data['pay_cat_model'] == 'cost':
        await Pay.create_cost(summ=data['pay_sum'], comment=comment, cat=data['pay_cat_id'])
        txt = '_Дані успішно внесені, переглянути усі витрати можна тут 👉 /costs_'
    elif data['pay_cat_model'] == 'income':
        await Pay.create_income(summ=data['pay_sum'], comment=comment, cat=data['pay_cat_id'])
        txt = '_Дані успішно внесені, переглянути усі надходження можна тут 👉 /incomes_'
    await state.reset_state()
    return txt
