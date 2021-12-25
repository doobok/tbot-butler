from aiogram import types
from aiogram.dispatcher import FSMContext

from states.mane import CatEdit
from utils.db.categories import Category
from utils.keyboards.category_kbd import categories_list, select_cat_type, confirm_new_cat, go_to_root
from utils.keyboards.global_kbd import go_to_main
from utils.misc.menu_utils import menu_str


async def category_list(msg: types.Message, state: FSMContext):
    await CatEdit.in_menu.set()
    model = 'another'
    if msg.text == menu_str['cat-cost']:
        model = 'cost'
    elif msg.text == menu_str['cat-income']:
        model = 'income'
    await state.update_data(cat_model=model, parent_id=0)
    await msg.answer(f'Ви знаходитесь в розділі *{msg.text}*', reply_markup=go_to_main())
    cat = await Category.view_dir(external_id=msg.from_user.id, model=model, parent_id=0)
    await msg.answer('_Тут ви можете переглянути структуру категорій, додавати нові категорії/підкатегорії '
                     'та видаляти застарілі ☝️ видаляти можна лише порожні, не можна видаляти глобальні категорії\n\n'
                     'Для того, щоб додати категорію \- перейдіть в ту категорію, яка має бути батьківською для '
                     'неї та напишіть мені її назву\nКатегорії першого порядку розташовані в *Кореневій категорії*_',
                     reply_markup=categories_list(categories=cat, item=None))


async def category_list_select(query: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await query.answer()
    await CatEdit.in_menu.set()
    data = await state.get_data()
    model = data.get('cat_model')
    cat_id = int(callback_data['id'])
    await state.update_data(parent_id=cat_id)
    item = await Category.view(cat_id=cat_id)
    cat = await Category.view_dir(external_id=query.message.chat.id, model=model, parent_id=cat_id)
    if item:
        txt = '*%s* 👈 поточна категорія' % item.get('name')
    else:
        txt = '👉 Коренева категорія'
    await query.message.edit_text(txt)
    await query.message.edit_reply_markup(reply_markup=categories_list(categories=cat, item=item))


async def add_cat1(msg: types.Message, state: FSMContext):
    if len(msg.text) > 20:
        await msg.answer('Назва надто довга, придумайте коротшу')
    else:
        await state.update_data(new_cat_name=msg.text)
        await CatEdit.next()
        await msg.answer('Вкажіть тип категорії\n\n*Глобальна* чи *Приватна*\n\n'
                         'Будьте відповідальні, оскільки глобальні категорії будуть бачити усі зареєстровані учасники, '
                         'також глобальну категорію неможливо видалити, тому створюйте їх лише якщо повністю впевнені '
                         'в своїх діях', reply_markup=select_cat_type())


async def add_cat2(query: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await CatEdit.next()
    await query.answer()
    data = await state.get_data()
    cat_name = data.get('new_cat_name')
    cat_global = callback_data['type']
    await state.update_data(new_cat_type=cat_global)
    txt = f'Ви дійсно бажаєте додати категорію:\n*{cat_name}*?'
    await query.message.edit_text(txt)
    await query.message.edit_reply_markup(reply_markup=confirm_new_cat())


async def category_create(query: types.CallbackQuery, state: FSMContext):
    await query.answer()
    data = await state.get_data()
    cat_name = data.get('new_cat_name')
    cat_model = data.get('cat_model')
    parent_id = data.get('parent_id')
    cat_global = data.get('new_cat_type')
    await Category.create(name=str(cat_name), external_id=query.message.chat.id, model=cat_model,
                          parent_id=parent_id, global_state=cat_global)
    await CatEdit.in_menu.set()
    txt = 'Категорія успішно додана'
    await query.message.edit_text(txt)
    await query.message.edit_reply_markup(reply_markup=go_to_root())
