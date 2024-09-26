import pandas as pd
from funcs.utils import *


def synchronous_mark_price(conn, public_api, inst_type, **kwargs):
    columns = {
        'instType': 'inst_type',
        'instId': 'inst_id',
        'markPx': 'mark_px',
        'ts': 'ts'
    }
    dat = public_api.get_mark_price(instType=inst_type, **kwargs)['data']
    dat = pd.DataFrame(dat)
    dat = dat[columns.keys()]
    dat['ts'] = dat.ts.apply(from_timestamp)
    dat = dat.replace({'': None, '-': None})
    dat = dat.rename(columns=columns)
    conn.upsert_dat(dat=dat, tbl_name='mark_price')