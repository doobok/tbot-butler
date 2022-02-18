from aiogram.utils.callback_data import CallbackData


def currency_select(cd):
    callback = CallbackData('set-currency', 'code')
    if cd is None:
        return callback.filter()
    else:
        return callback.new(code=cd)
