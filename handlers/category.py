from aiogram import types
from aiogram.dispatcher import FSMContext

from states.mane import CatEdit
from utils.db.categories import Category
from utils.keyboards.category_kbd import categories_list, categories_menu
from utils.misc.menu_utils import menu_str


async def category_list(msg: types.Message, state: FSMContext):
    await CatEdit.in_menu.set()
    model = 'another'
    if msg.text == menu_str['cat-cost']:
        model = 'cost'
    elif msg.text == menu_str['cat-income']:
        model = 'income'
    await state.update_data(cat_model=model)
    await msg.answer(f'Ви знаходитесь в розділі *{msg.text}*', reply_markup=categories_menu())
    cat = await Category.view_dir(external_id=msg.from_user.id, model=model, parent_id=0)
    await msg.answer('Тут ви можете переглянути структуру категорій, додавати нові категорії/підкатегорії '
                     'та видаляти застарілі видаляти можна лише порожні',
                     reply_markup=categories_list(categories=cat, item=None))


async def category_list_select(query: types.CallbackQuery, state: FSMContext, callback_data: dict):
    data = await state.get_data()
    model = data.get('cat_model')
    cat_id = int(callback_data['id'])
    item = await Category.view(cat_id=cat_id)
    cat = await Category.view_dir(external_id=query.message.chat.id, model=model, parent_id=cat_id)
    if item:
        txt = '*%s* 👈 поточна категорія' % item.get('name')
    else:
        txt = '👉 Коренева категорія'
    await query.message.edit_text(txt)
    await query.message.edit_reply_markup(reply_markup=categories_list(categories=cat, item=item))


async def category_create(msg: types.Message, state: FSMContext):
    await Category.create(name='cat1', external_id=msg.from_user.id, model='cost', parent_id=1, global_state=False)
