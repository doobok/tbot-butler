import datetime

from utils.db.storage import MysqlConnection


class Pay(MysqlConnection):
    @staticmethod
    async def create_cost(summ: float, comment: str, cat: int, uid: int):
        sql = 'INSERT INTO `costs` (`sum`, `comment`, `cat`, `external_id`) ' \
              'VALUES (%s, %s, %s, %s)'
        params = (summ, comment, cat, uid)
        await Pay._make_request(sql, params)

    @staticmethod
    async def create_income(summ: float, comment: str, cat: int, uid: int):
        sql = 'INSERT INTO `incomes` (`sum`, `comment`, `cat`, `external_id`) ' \
              'VALUES (%s, %s, %s, %s)'
        params = (summ, comment, cat, uid)
        await Pay._make_request(sql, params)

    @staticmethod
    async def pay_comment_add(model: str, comment: str, uid: int):
        sql = 'UPDATE %s SET comment = \'%s\' WHERE external_id = %s ORDER BY id DESC LIMIT 1' \
              % (model, comment, uid)
        await Pay._make_request(sql)

    @staticmethod
    async def pays(start: int, end: int, model: str, uid: int):
        sql = 'SELECT * FROM %s JOIN `categories` ON %s.cat = categories.id WHERE %s.external_id = %s ' \
              'ORDER BY %s.id DESC LIMIT %s, %s' % (model, model, model, uid, model, start, end)
        return await Pay._make_request(sql, mult=True, fetch=True)

    @staticmethod
    async def is_fresh(pid: int, model: str) -> bool:
        lock_date = datetime.datetime.now() - datetime.timedelta(days=1)
        sql = 'SELECT * FROM %s WHERE id = %s AND time > \'%s\'' % (model, pid, lock_date)
        res = await Pay._make_request(sql, fetch=True)
        return bool(res)

    @staticmethod
    async def delete(pay_id: int, model: str, uid: int):
        sql = 'DELETE FROM %s WHERE %s.id = %s AND `external_id` = %s' % (model, model, pay_id, uid)
        return await Pay._make_request(sql)
