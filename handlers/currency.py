import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode

from states.mane import CurrencySection
from utils.db.currency_db import Currency
from utils.keyboards.currency_kbd import currency_menu, currency_list
from utils.misc.currency_utils import currency
from utils.requests.currency_requests import CurrencyRequest


async def opn_currency(msg: types.Message, state: FSMContext):
    await CurrencySection.in_currency.set()
    result = await Currency.get_currency(msg)
    cu = result.get('currency')
    if cu is not None:
        currency_code = currency[cu]
        currencies = await CurrencyRequest.get_mono_curr()
        cr = next(x for x in currencies if x['currencyCodeA'] == cu)
        if cr.get('rateSell', False):
            multiply = cr.get('rateSell', 0)
        else:
            multiply = cr.get('rateCross', 0)
        await state.update_data(currency_mult=multiply)
        await state.update_data(currency_code=currency_code)
        txt = f'👨‍🦳 Поточна валюта для конветрації - <b>{currency_code}</b>\nпоточний курс <b>{multiply}</b> ' \
              f'щойно оновлений, можете вводити суму для конветрації'
    else:
        txt = '💁‍♂️️ Для початку потрібно обрати валюту'
    await msg.answer(txt, parse_mode=ParseMode.HTML, reply_markup=currency_menu())


async def menu_currency(msg: types.Message, state: FSMContext):
    await msg.answer(f'Оберіть валюту для конвертації', reply_markup=currency_list())


async def select_currency(query: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await query.answer()
    currencies = await CurrencyRequest.get_mono_curr()
    if type(currencies) is not list:
        await query.message.edit_text('⚠️ Невдача при отримані актуального курсу валюти, спробуйте повторити спробу '
                                      'пізніше')
    else:
        currency_code = int(callback_data['code'])
        cu = currency[currency_code]
        await Currency.upd_currency(query.from_user.id, currency_code)

        cr = next(x for x in currencies if x['currencyCodeA'] == currency_code)
        if cr.get('rateSell', False):
            multiply = cr.get('rateSell', 0)
        else:
            multiply = cr.get('rateCross', 0)
        await state.update_data(currency_mult=multiply)
        await state.update_data(currency_code=currency_code)
        txt = f'Ви обрали <b>{cu}</b> актуальний курс <b>{multiply}</b>\nвведіть суму, щоб конвертувати в гривню\nвалюту ' \
              f'можна в будь-який час змінити використовуючи меню '
        await query.message.edit_text(txt, parse_mode=ParseMode.HTML)


async def use_currency(msg: types.Message, state: FSMContext):
    val = list(map(float, re.findall(r"""\d+ # one or more digits
                                  (?: # followed by...
                                      \. # a decimal point 
                                      \d+ # and another set of one or more digits
                                  )? # zero or one times""",
                                     msg.text,
                                     re.VERBOSE)))
    if len(val) < 1:
        await msg.answer('Будь\-ласка, введіть число')
    else:
        summa = val[0]
        data = await state.get_data()
        multiply = data.get('currency_mult', 0)
        currency_code = data.get('currency_code', 0)
        result = summa * multiply
        code = currency[currency_code]
        if multiply > 0:
            txt = f'🧾 Результат <b>{result}</b> грн. за <b>{summa}</b> {code}\nкурс <i>{multiply}</i>'
        else:
            txt = 'Для початку оберіть валюту'
        await msg.answer(txt, parse_mode=ParseMode.HTML)
