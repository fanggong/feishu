import pandas as pd
from funcs.utils import *


def _get_fills_history(trade_api, inst_type, **kwargs):
    dat = trade_api.get_fills_history(instType=inst_type, **kwargs).get('data')
    if len(dat) == 0:
        return dat
    else:
        kwargs['after'] = dat[-1]['billId']
        dat = dat + _get_fills_history(trade_api, inst_type, **kwargs)
        return dat


def synchronous_fills_history(conn, path=None, trade_api=None, **kwargs):
    columns = {
        'instType': 'inst_type',
        'instId': 'inst_id',
        'tradeId': 'trade_id',
        'ordId': 'ord_id',
        'clOrdId': 'cl_ord_id',
        'billId': 'bill_id',
        'tag': 'tag',
        'fillPx': 'fill_px',
        'fillSz': 'fill_sz',
        'side': 'side',
        'posSide': 'pos_side',
        'execType': 'exec_type',
        'feeCcy': 'fee_ccy',
        'fee': 'fee',
        'ts': 'ts',
        'subType': 'sub_type'
    }
    if path:
        dat = pd.read_csv(path)
    else:
        dat = []
        for inst_type in ['SPOT', 'SWAP', 'MARGIN']:
            tmp = _get_fills_history(trade_api=trade_api, inst_type=inst_type, **kwargs)
            dat = dat + tmp
        dat = pd.DataFrame(dat)
        dat = dat[columns.keys()]
    dat['ts'] = dat.ts.apply(from_timestamp)
    dat = dat.rename(columns=columns)
    conn.upsert_dat(dat=dat, tbl_name='fills_history')

