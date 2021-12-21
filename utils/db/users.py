from aiogram import types

from utils.db.storage import MysqlConnection


class User(MysqlConnection):
    @staticmethod
    async def is_new(msg: types.Message) -> bool:
        sql = 'SELECT * FROM `users` WHERE `external_id` = %s'
        params = (msg.contact.user_id,)
        res = await User._make_request(sql, params, fetch=True)
        return not bool(res)

    @staticmethod
    async def is_guest(msg: types.Message) -> bool:
        sql = 'SELECT * FROM `users` WHERE `external_id` = %s'
        params = (msg.from_user.id,)
        res = await User._make_request(sql, params, fetch=True)
        return not bool(res)

    @staticmethod
    async def register(uid: int, name: str):
        sql = 'INSERT INTO `users` (`external_id`, `name`, `role`) ' \
              'VALUES (%s, %s, %s)'
        params = (uid, name, 'user')
        await User._make_request(sql, params)

    @staticmethod
    async def get_user(msg: types.Message) -> bool:
        sql = 'SELECT * FROM `users` WHERE `external_id` = %s'
        params = (msg.from_user.id,)
        return await User._make_request(sql, params, fetch=True)
