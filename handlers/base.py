from aiogram import types
from aiogram.dispatcher import FSMContext

from data import config
from states.mane import UserAdd
from utils.db.users import User
from utils.keyboards.global_kbd import main_menu, cancel_menu, confirm_add_user, go_to_main


async def bot_start(msg: types.Message, state: FSMContext):
    await msg.answer('Прехорошого дня! \nБажаєте внести видаток, або дохід?', reply_markup=main_menu())


async def bot_restart(msg: types.Message, state: FSMContext):
    await state.reset_state(with_data=False)
    await msg.answer('Оберіть пункт меню', reply_markup=main_menu())


async def add_user1(msg: types.Message, state: FSMContext):
    await UserAdd.wait_for_contact.set()
    await msg.answer('Відправте мені контакт користувача, щоб я зміг внести його в список запрошених',
                     reply_markup=cancel_menu())


async def add_user2(msg: types.Message, state: FSMContext):
    if msg.chat.id == int(config.admin):
        if msg.contact.user_id:
            if await User.is_new(msg):
                await state.update_data(new_uid=msg.contact.user_id)
                await UserAdd.next()
                await msg.answer('Як я можу звертатися до користувача?')
            else:
                await msg.answer('Користувач вже зареєстрований')
        else:
            await msg.answer('Контакт не зареєстрований в Телеграм')


async def add_user3(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    uid = data.get('new_uid')
    await state.update_data(new_uname=msg.text)
    await UserAdd.next()
    txt = [
        'Зведена інформація:',
        f'id: *{uid}*',
        f'ім\'я: *{msg.text}*',
        'Додати користувача?'
    ]
    await msg.answer('\n\n'.join(txt), reply_markup=confirm_add_user())


async def add_user4(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    uid = data.get('new_uid')
    uname = data.get('new_uname')
    await User.register(uid, uname)
    await state.reset_state(with_data=False)
    await msg.answer('Користувач успішно доданий до списку запрошених', reply_markup=go_to_main())
