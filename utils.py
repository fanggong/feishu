import datetime
import lark_oapi as lark
import time
import pandas as pd

from config import *
from database.Mysql import MysqlEngine
from okx.Trade import TradeAPI
from okx.Account import AccountAPI
from okx.Funding import FundingAPI
from okx.PublicData import PublicAPI
from okx.MarketData import MarketAPI
from feishu.FeishuAppRobot import FeishuAppRobot
from yinbao.Store import StoreApi
from yinbao.Sales import SalesApi
from yinbao.Products import ProductsApi
from yinbao.Customers import CustomersApi
from funcs import *

INTERACTIVE_CARD = {
    'crypto_report': {'id': 'AAq7F02QhXIfo', 'version_name': '1.0.9'},
    'risk_report': {'id': 'AAq7xvyDvK3WX', 'version_name': '1.0.3'}
}

app_id = FEISHU_CONFIG['LongQi']['app_id']
app_secret = FEISHU_CONFIG['LongQi']['app_secret']

app_id_BC = FEISHU_CONFIG['BC']['app_id']
app_secret_BC = FEISHU_CONFIG['BC']['app_secret']

yinbao_app_id = YINBAO_CONFIG['app_id']
yinbao_app_key = YINBAO_CONFIG['app_key']

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


store_api = StoreApi(app_id=yinbao_app_id, app_key=yinbao_app_key)
sales_api = SalesApi(app_id=yinbao_app_id, app_key=yinbao_app_key)
products_api = ProductsApi(app_id=yinbao_app_id, app_key=yinbao_app_key)
customer_api = CustomersApi(app_id=yinbao_app_id, app_key=yinbao_app_key)


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


def get_yesterday(dt: datetime.datetime):
    dt = dt - datetime.timedelta(days=1)
    return dt.strftime('%Y-%m-%d %H:%M:%S')


def update_log(conn: MysqlEngine, s, f, role):
    dat = pd.DataFrame({
        'update_at': [now()],
        'num_all': [s + f],
        'num_success': [s],
        'num_fail': [f],
        'role': role
    })
    conn.append_dat(dat=dat, tbl_name='update_log')


if __name__ == '__main__':
    # tmp = sales_api.get_tickets(start_time='2024-09-29 00:00:00', end_time='2024-10-05 00:00:01')
    # tmp = store_api.get_store_list()
    synchronous_customers(conn=conn, customer_api=customer_api)