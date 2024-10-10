from database.Mysql import MysqlEngine
from funcs.utils import *


def datapush_sales_report(conn: MysqlEngine):
    today_m30 = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    today = datetime.now().strftime('%Y-%m-%d')
    res = {
        'today_m30': today_m30,
        'today': today
    }
    return res