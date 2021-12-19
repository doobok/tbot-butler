from aiogram import types

from utils.db.storage import MysqlConnection


class User(MysqlConnection):
    @staticmethod
    async def is_new(msg: types.Message) -> bool:
        sql = 'SELECT `id` FROM `users` WHERE `external_id` = %s'
        params = (msg.contact.user_id,)
        r = await User._make_request(sql, params, fetch=True)
        return not bool(r)

    @staticmethod
    async def register(msg: types.Message):
        sql = 'INSERT INTO `users` (`first_name`, `external_id`, `phone`, `last_name`, `role`, `role_id`) ' \
              'VALUES (%s, %s, %s, %s, %s, %s)'
        params = (msg.from_user.first_name, msg.from_user.id, msg.from_user.id, msg.from_user.last_name,
                  msg.from_user.last_name, msg.from_user.id)
        await User._make_request(sql, params)
