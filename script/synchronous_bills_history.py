import time
import pandas as pd
from .utils import *


def _get_bills_history(account_api, **kwargs):
    dat = account_api.get_account_bills_archive(**kwargs).get('data')
    time.sleep(0.4)
    if len(dat) == 0:
        return dat
    else:
        kwargs['after'] = dat[-1]['billId']
        dat = dat + _get_bills_history(account_api, **kwargs)
        return dat


def synchronous_bills_history(conn, path=None, account_api=None, **kwargs):
    columns = {
        'instType': 'inst_type',
        'billId': 'bill_id',
        'subType': 'sub_type',
        'ts': 'ts',
        'balChg': 'bal_chg',
        'posBalChg': 'pos_bal_chg',
        'bal': 'bal',
        'posBal': 'pos_bal',
        'sz': 'sz',
        'px': 'px',
        'ccy': 'ccy',
        'pnl': 'pnl',
        'fee': 'fee',
        'mgnMode': 'mgn_mode',
        'instId': 'inst_id',
        'ordId': 'ord_id',
        'execType': 'exec_type',
        'interest': 'interest',
        'tag': 'tag',
        'fillTime': 'fill_time',
        'tradeId': 'trade_id',
        'clOrdId': 'cl_ord_id',
        'fillIdxPx': 'fill_idx_px',
        'fillMarkPx': 'fill_mark_px',
        'fillPxVol': 'fill_px_vol',
        'fillPxUsd': 'fill_px_usd',
        'fillMarkVol': 'fill_mark_vol',
        'fillFwdPx': 'fill_fwd_px'
    }
    if path:
        dat = pd.read_csv(path)
    else:
        dat = _get_bills_history(account_api=account_api, **kwargs)
        dat = pd.DataFrame(dat)
        dat = dat[columns.keys()]
    dat['billId'] = dat.billId.str.replace("'", '')
    dat['ordId'] = dat.ordId.str.replace("'", '')
    dat['clOrdId'] = dat.clOrdId.str.replace("'", '')
    dat['tradeId'] = dat.tradeId.str.replace("'", '')
    dat['ts'] = dat.ts.apply(from_timestamp)
    dat['fillTime'] = dat.fillTime.apply(from_timestamp)
    dat = dat.replace({'': None, '-': None})
    dat = dat.rename(columns=columns)
    conn.upsert_dat(dat=dat, tbl_name='bills_history')


