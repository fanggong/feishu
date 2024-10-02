import datetime
import lark_oapi as lark
import time
import pandas as od
from config import *
from database.Mysql import MysqlEngine
from okx.Trade import TradeAPI
from okx.Account import AccountAPI
from okx.Funding import FundingAPI
from okx.PublicData import PublicAPI
from okx.MarketData import MarketAPI
from feishu.FeishuAppRobot import FeishuAppRobot
from funcs import *


app_id = FEISHU_CONFIG['LongQi']['app_id']
app_secret = FEISHU_CONFIG['LongQi']['app_secret']

api_key = OKX_CONFIG['api_key']
secret_key = OKX_CONFIG['secret_key']
passphrase = OKX_CONFIG['passphrase']

conn = MysqlEngine(
    user_name=DB_CONFIG['mysql']['username'], password=DB_CONFIG['mysql']['password'],
    host=DB_CONFIG['mysql']['host'], port=DB_CONFIG['mysql']['port'],
    database=DB_CONFIG['mysql']['database']
)
trade_api = TradeAPI(api_key, secret_key, passphrase, False, '0')
account_api = AccountAPI(api_key, secret_key, passphrase, False, '0')
funding_api = FundingAPI(api_key, secret_key, passphrase, False, '0')
public_api = PublicAPI(api_key, secret_key, passphrase, False, '0')
market_api = MarketAPI(api_key, secret_key, passphrase, False, '0')
feishu_app_robot = FeishuAppRobot(app_id=app_id, app_secret=app_secret)


def send_text_msg_to_myself(content):
    content = lark.JSON.marshal({'text': content})
    feishu_app_robot.send_msg(receive_id=OPEN_ID['Fang Yongchao'], msg_type='text', content=content)


def send_interactive_card_to_my_self(template_variable, template_id, template_version_name):
    content = {
        'type': 'template',
        'data': {
            'template_id': template_id,
            'template_version_name': template_version_name,
            'template_variable': template_variable
        }
    }
    content = lark.JSON.marshal(content)
    feishu_app_robot.send_msg(receive_id=OPEN_ID['Fang Yongchao'], msg_type='interactive', content=content)


def now():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def get_quarter_firstday(dt: datetime.datetime):
    month = dt.month
    month = month - (month - 1) % 3
    dt = dt.replace(month=month, day=1, hour=0, minute=0, second=0, microsecond=0)
    return dt.strftime('%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    send_interactive_card_to_my_self(
        template_variable=datapush_crypto_report(conn=conn),
        template_id=INTERACTIVE_CARD['crypto_report']['id'],
        template_version_name=INTERACTIVE_CARD['crypto_report']['version_name']
    )