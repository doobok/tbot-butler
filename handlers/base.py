from aiogram import types
from aiogram.dispatcher import FSMContext


async def bot_start(msg: types.Message, state: FSMContext):
    await state.update_data(test='test string')
    await msg.answer('Say hello')
