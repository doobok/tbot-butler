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
    async def pays(start: int, end: int, model: str, uid: int):
        sql = 'SELECT * FROM %s JOIN `categories` ON %s.cat = categories.id WHERE %s.external_id = %s ' \
              'ORDER BY %s.id DESC LIMIT %s, %s' % (model, model, model, uid, model, start, end)
        return await Pay._make_request(sql, mult=True, fetch=True)

    @staticmethod
    async def delete(pay_id: int, model: str, uid: int):
        sql = 'DELETE FROM %s WHERE %s.id = %s AND `external_id` = %s' % (model, model, pay_id, uid)
        return await Pay._make_request(sql)
