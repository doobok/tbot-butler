import os
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
BASE_URL = os.getenv('BASE_URL')  # Webhook domain
WEBHOOK_PATH = f'/tg/webhooks/bot/{BOT_TOKEN}'
WEBHOOK_URL = f'{BASE_URL}{WEBHOOK_PATH}'

WEBAPP_HOST = os.getenv('LOCAL_IP')  # or ip
WEBAPP_PORT = os.getenv('WEBAPP_PORT')

admin = os.getenv('ADMIN_ID')

ip = {
    'db':    os.getenv('LOCAL_IP'),
    'redis': os.getenv('LOCAL_IP'),
}
mysql_info = {
    'host':     ip['db'],
    'user':     os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'db':       os.getenv('DB_NAME'),
    'maxsize':  int(os.getenv('DB_MAX_SIZE')),
    'port':     int(os.getenv('DB_PORT')),
}
redis = {
    'address':  ip['redis'],
    'password': os.getenv('REDIS_PASSWORD'),
    'db': os.getenv('REDIS_DB'),
}

