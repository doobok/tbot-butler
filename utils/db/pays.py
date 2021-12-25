from utils.db.storage import MysqlConnection


class Pay(MysqlConnection):
    @staticmethod
    async def create_cost(summ: float, comment: str, cat: int):
        sql = 'INSERT INTO `costs` (`sum`, `comment`, `cat`) ' \
              'VALUES (%s, %s, %s)'
        params = (summ, comment, cat)
        await Pay._make_request(sql, params)\


    @staticmethod
    async def create_income(summ: float, comment: str, cat: int):
        sql = 'INSERT INTO `incomes` (`sum`, `comment`, `cat`) ' \
              'VALUES (%s, %s, %s)'
        params = (summ, comment, cat)
        await Pay._make_request(sql, params)
