from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart

from handlers.base import bot_start, add_user


def setup(dp: Dispatcher):
    dp.register_message_handler(bot_start, CommandStart(), state="*")
    dp.register_message_handler(add_user, content_types='contact', state="*")
