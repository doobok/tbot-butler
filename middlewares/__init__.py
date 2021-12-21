from aiogram import Dispatcher

from .member import MemberMiddleware


def setup(dp: Dispatcher):
    dp.middleware.setup(MemberMiddleware())
