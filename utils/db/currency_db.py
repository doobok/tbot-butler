from aiogram import types

from utils.db.storage import MysqlConnection


class Currency(MysqlConnection):
    @staticmethod
    async def upd_currency(uid: int, cu: int):
        sql = 'UPDATE users SET currency = %s WHERE users.external_id = %s' % (cu, uid)
        await Currency._make_request(sql)

    @staticmethod
    async def get_currency(msg: types.Message):
        sql = 'SELECT currency FROM users WHERE external_id = %s' % msg.from_user.id
        return await Currency._make_request(sql, fetch=True)
