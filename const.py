from config import *

MAX_RETRY = 5

# feishu interactive card
INTERACTIVE_CARD = {
    'crypto_report': {'id': 'AAq7F02QhXIfo', 'version_name': '1.0.9'},
    'risk_report': {'id': 'AAq7xvyDvK3WX', 'version_name': '1.0.3'},
    'sales_report': {'id': 'AAq7QaZZ15OqP', 'version_name': '1.0.12'}
}

# feishu app
CRYPTO_APP_NAME = 'LongQi'
BAR_APP_NAME = 'BC'
APP_ID_CRYPTO = FEISHU_CONFIG['crypto']['app_id']
APP_SECRET_CRYPTO = FEISHU_CONFIG['crypto']['app_secret']
APP_ID_BAR = FEISHU_CONFIG['bar']['app_id']
APP_SECRET_BAR = FEISHU_CONFIG['bar']['app_secret']

# yinbao
APP_ID_YINBAO = YINBAO_CONFIG['app_id']
APP_KEY_YINBAO = YINBAO_CONFIG['app_key']

# okx
API_KEY = OKX_CONFIG['api_key']
SECRET_KEY = OKX_CONFIG['secret_key']
PASSPHRASE = OKX_CONFIG['passphrase']

# database
USERNAME = DB_CONFIG['mysql']['username']
PASSWORD = DB_CONFIG['mysql']['password']
HOST = DB_CONFIG['mysql']['host']
PORT = DB_CONFIG['mysql']['port']
DATABASE = DB_CONFIG['mysql']['database']

# my info
MY_USER_ID = USER_ID['Fang Yongchao']

# moralis
API_KEY_MORALIS = MORALIS_CONFIG['api_key']

