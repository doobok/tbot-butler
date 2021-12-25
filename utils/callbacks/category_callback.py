from aiogram.utils.callback_data import CallbackData


def cat_list_item(cat_id):
    callback = CallbackData('category', 'id')
    if cat_id is None:
        return callback.filter()
    else:
        return callback.new(id=cat_id)


def cat_item_global(tp):
    callback = CallbackData('cat-type', 'type')
    if tp is None:
        return callback.filter()
    else:
        return callback.new(type=tp)


def confirm(approve):
    callback = CallbackData('cat-type', 'approve')
    if approve is None:
        return callback.filter()
    else:
        return callback.new(approve=approve)


def remove(uid):
    callback = CallbackData('remove', 'id')
    if uid is None:
        return callback.filter()
    else:
        return callback.new(id=uid)
