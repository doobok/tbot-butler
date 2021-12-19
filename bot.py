import argparse
import logging

from aiogram import Bot, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.webhook import SendMessage
from aiogram.utils.executor import start_webhook

from data import config

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.BOT_TOKEN)
storage = RedisStorage2(
    config.redis['address'], 6379,
    password=config.redis['password'],
    db=config.redis['db'],
    pool_size=10, prefix='butler')
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())


async def on_startup(dp):
    import handlers
    handlers.setup(dp)
    await bot.set_webhook(config.WEBHOOK_URL)
    # insert code here to run it after start


async def on_shutdown(dp):
    logging.warning('Shutting down..')

    # insert code here to run it before shutdown

    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()

    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning('Bye!')

if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=config.WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        # skip_updates=True,
        host=config.WEBAPP_HOST,
        port=config.WEBAPP_PORT,

    )
