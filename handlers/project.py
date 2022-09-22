from aiogram import types
from aiogram.dispatcher import FSMContext


async def projects_list(msg: types.Message, state: FSMContext):
    await msg.answer(f'Перелік проектів', )
