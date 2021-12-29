import asyncio

from aiogram import types, Dispatcher
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware

from utils.db.users import User


class MemberMiddleware(BaseMiddleware):
    """
    Simple middleware
    """

    def __init__(self):
        super(MemberMiddleware, self).__init__()

    async def on_process_message(self, msg: types.Message, data: dict):
        # handler = current_handler.get()
        dispatcher = Dispatcher.get_current()
        state = dispatcher.current_state()
        data = await state.get_data()
        print(data)
        if data.get('is_member', False) is False:
            print('check')
            if await User.is_guest(msg):
                print('locked')
                raise CancelHandler()
            else:
                print('set member')
                await state.update_data(is_member=True)

        # else:
        #     data = await state.get_data()
        #     await state.update_data(new_uid=msg.contact.user_id)
