import os
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
BASE_URL = os.getenv('BASE_URL')  # Webhook domain
WEBHOOK_PATH = f'/tg/webhooks/bot/{BOT_TOKEN}'
WEBHOOK_URL = f'{BASE_URL}{WEBHOOK_PATH}'

WEBAPP_HOST = '0.0.0.0'  # or ip
WEBAPP_PORT = 8082

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
    'address':  'redis://' + ip['redis'],
    'password': os.getenv('REDIS_PASSWORD')
}

