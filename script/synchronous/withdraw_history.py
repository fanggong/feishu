import time
import pandas as pd
from script.utils import *


def _get_withdraw_history(funding_api, **kwargs):
    dat = funding_api.get_withdrawal_history(**kwargs).get('data')
    time.sleep(0.2)
    if len(dat) == 0:
        return dat
    else:
        kwargs['after'] = dat[-1]['ts']
        dat = dat + _get_withdraw_history(funding_api, **kwargs)
        return dat


def synchronous_withdraw_history(conn, funding_api=None, **kwargs):
    columns = {
        'chain': 'chain',
        'areaCodeFrom': 'area_code_from',
        'clientId': 'client_id',
        'fee': 'fee',
        'amt': 'amt',
        'txId': 'tx_id',
        'areaCodeTo': 'area_code_to',
        'ccy': 'ccy',
        'from': 'from',
        'to': 'to',
        'state': 'state',
        'nonTradableAsset': 'non_tradable_asset',
        'ts': 'ts',
        'wdId': 'wd_id',
        'feeCcy': 'fee_ccy'
    }
    dat = _get_withdraw_history(funding_api=funding_api, **kwargs)
    dat = pd.DataFrame(dat)
    dat = dat[columns.keys()]
    dat['ts'] = dat.ts.apply(from_timestamp)
    dat = dat.replace({'': None, '-': None})
    dat = dat.rename(columns=columns)
    conn.upsert_dat(dat=dat, tbl_name='withdraw_history')


