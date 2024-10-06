from funcs.const import EXCHANGE_RATE
from funcs.utils import *
from database.Mysql import MysqlEngine
from okx.MarketData import MarketAPI


def synchronous_exchange_rate(conn: MysqlEngine, market_api: MarketAPI):
    columns = {
        'usdCny': 'usd_cny'
    }
    dat = market_api.get_exchange_rate()['data']
    dat = pd.DataFrame(dat)
    dat = dat[columns.keys()]
    dat = dat.rename(columns=columns)
    conn.replace_dat(dat=dat, tbl_name=EXCHANGE_RATE)