from utils.db.storage import MysqlConnection


class Category(MysqlConnection):
    @staticmethod
    async def create(name: str, external_id: int, model: str, parent_id: int, global_state: bool):
        sql = 'INSERT INTO `categories` (`name`, `external_id`, `model`, `parent_id`, `global`) ' \
              'VALUES (%s, %s, %s, %s, %s)'
        params = (name, external_id, model, parent_id, global_state)
        await Category._make_request(sql, params)

    @staticmethod
    async def view_dir(external_id: int, model: str, parent_id: int):
        sql = 'SELECT * FROM `categories` WHERE (`external_id` = %s OR `global` = 1) AND ' \
              '`parent_id` = %s AND `model` LIKE %s'
        params = (external_id, parent_id, model)
        return await Category._make_request(sql, params, mult=True, fetch=True)

    @staticmethod
    async def view(cat_id: int):
        sql = 'SELECT * FROM `categories` WHERE `id` = %s'
        params = (cat_id,)
        return await Category._make_request(sql, params, fetch=True)
