import pandas as pd
from funcs.utils import *


def synchronous_exchange_rate(conn, market_api):
    columns = {
        'usdCny': 'usd_cny'
    }
    dat = market_api.get_exchange_rate()['data']
    dat = pd.DataFrame(dat)
    dat = dat[columns.keys()]
    dat = dat.rename(columns=columns)
    conn.replace_dat(dat=dat, tbl_name='exchange_rate')