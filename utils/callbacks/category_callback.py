from aiogram.utils.callback_data import CallbackData


def cat_list_item(cat_id):
    callback = CallbackData('category', 'id')
    if cat_id is None:
        return callback.filter()
    else:
        return callback.new(id=cat_id)


def del_cat_item(cat_id):
    callback = CallbackData('del-category', 'id')
    if cat_id is None:
        return callback.filter()
    else:
        return callback.new(id=cat_id)