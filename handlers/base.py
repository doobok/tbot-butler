from aiogram import types
from aiogram.dispatcher import FSMContext

from data import config
from utils.db.users import User


async def bot_start(msg: types.Message, state: FSMContext):
    await User.register(msg)
    await state.update_data(test='test string')
    await msg.answer('Say hello')


async def add_user(msg: types.Message, state: FSMContext):
    if msg.chat.id == int(config.admin):
        if msg.contact.user_id:
            if await User.is_new(msg):
                await msg.answer('Користувач вже зареєстрований')
            else:
                print(msg.contact.user_id)
                print(msg)
                await msg.answer('Користувач успішно зареєстрований, можна починати користуватись ботом')
        else:
            await msg.answer('Контакт не зареєстрований в Телеграм')
