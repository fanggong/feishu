import datetime
import lark_oapi as lark
import time
import pandas as pd

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
from yinbao.Access import AccessApi
from funcs import *

from const import *

# database connection
CONN = MysqlEngine(user_name=USERNAME, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)

# okx api client
TRADE_API = TradeAPI(API_KEY, SECRET_KEY, PASSPHRASE, False, '0')
ACCOUNT_API = AccountAPI(API_KEY, SECRET_KEY, PASSPHRASE, False, '0')
FUNDING_API = FundingAPI(API_KEY, SECRET_KEY, PASSPHRASE, False, '0')
PUBLIC_API = PublicAPI(API_KEY, SECRET_KEY, PASSPHRASE, False, '0')
MARKET_API = MarketAPI(API_KEY, SECRET_KEY, PASSPHRASE, False, '0')

# feishu app robot
FEISHU_APP_ROBOT_CRYPTO = FeishuAppRobot(app_id=APP_ID_CRYPTO, app_secret=APP_SECRET_CRYPTO, name=CRYPTO_APP_NAME)
FEISHU_APP_ROBOT_BAR = FeishuAppRobot(app_id=APP_ID_BAR, app_secret=APP_SECRET_BAR, name=BAR_APP_NAME)

# yinbao api client
STORE_API = StoreApi(app_id=APP_ID_YINBAO, app_key=APP_KEY_YINBAO)
SALES_API = SalesApi(app_id=APP_ID_YINBAO, app_key=APP_KEY_YINBAO)
PRODUCTS_API = ProductsApi(app_id=APP_ID_YINBAO, app_key=APP_KEY_YINBAO)
CUSTOMERS_API = CustomersApi(app_id=APP_ID_YINBAO, app_key=APP_KEY_YINBAO)
ACCESS_API = AccessApi(app_id=APP_ID_YINBAO, app_key=APP_KEY_YINBAO)


def send_text_msg_to_myself(robot: FeishuAppRobot, content: str) -> None:
    content = lark.JSON.marshal({'text': content})
    robot.send_msg(receive_id=MY_USER_ID, msg_type='text', content=content)


def send_interactive_card_to_my_self(robot: FeishuAppRobot, template_variable: str, template_id: str,
                                     template_version_name: str) -> None:
    content = {
        'type': 'template',
        'data': {
            'template_id': template_id,
            'template_version_name': template_version_name,
            'template_variable': template_variable
        }
    }
    content = lark.JSON.marshal(content)
    robot.send_msg(receive_id=MY_USER_ID, msg_type='interactive', content=content)


def str_now() -> str:
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def get_quarter_firstday(dt: datetime.datetime) -> str:
    month = dt.month
    month = month - (month - 1) % 3
    dt = dt.replace(month=month, day=1, hour=0, minute=0, second=0, microsecond=0)
    return dt.strftime('%Y-%m-%d %H:%M:%S')


def get_yesterday(dt: datetime.datetime) -> str:
    dt = dt - datetime.timedelta(days=1)
    return dt.strftime('%Y-%m-%d %H:%M:%S')


def update_log(conn: MysqlEngine, s: int, f: int, role: str):
    dat = pd.DataFrame({
        'update_at': str_now(),
        'num_all': s + f,
        'num_success': s,
        'num_fail': f,
        'role': role
    }, index=[0])
    conn.append_dat(dat=dat, tbl_name=UPDATE_LOG)


if __name__ == '__main__':
    synchronous_tickets(conn=CONN, sales_api=SALES_API, start_time='2024-10-11 13:30:00', end_time='2024-10-12 13:30:00')
    # tmp = ACCESS_API.get_daily_access_times_log(start_date='2024-10-12', end_date='2024-10-12')
    # print(tmp)