from database.Mysql import MysqlEngine
from funcs.utils import *


def datapush_sales_report(conn: MysqlEngine, start_date=None, end_date=None, period=None):
    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d') if not start_date else start_date
    end_date = datetime.now().strftime('%Y-%m-%d') if not end_date else end_date
    period = 1 if not period else period
    res = {
        'start_date': start_date,
        'end_date': end_date,
        'period': period,
        'graph': {}
    }
    return res