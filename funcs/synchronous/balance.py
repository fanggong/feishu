import pandas as pd
from funcs.utils import *
from okx.Account import AccountAPI
from database.Mysql import MysqlEngine


def synchronous_balance(conn: MysqlEngine, account_api: AccountAPI, **kwargs):
    columns = {
        'accAvgPx': 'acc_avg_px',
        'availBal': 'avail_bal',
        'availEq': 'avail_eq',
        'borrowFroz': 'borrow_froz',
        'cashBal': 'cash_bal',
        'ccy': 'ccy',
        'clSpotInUseAmt': 'cl_spot_in_use_amt',
        'crossLiab': 'cross_liab',
        'disEq': 'dis_eq',
        'eq': 'eq',
        'eqUsd': 'eq_usd',
        'fixedBal': 'fixed_bal',
        'frozenBal': 'frozen_bal',
        'imr': 'imr',
        'interest': 'interest',
        'isoEq': 'iso_eq',
        'isoLiab': 'iso_liab',
        'isoUpl': 'iso_upl',
        'liab': 'liab',
        'maxLoan': 'max_loan',
        'maxSpotInUse': 'max_spot_in_use',
        'mgnRatio': 'mgn_ratio',
        'mmr': 'mmr',
        'notionalLever': 'notional_lever',
        'openAvgPx': 'open_avg_px',
        'ordFrozen': 'ord_frozen',
        'rewardBal': 'reward_bal',
        'smtSyncEq': 'smt_sync_eq',
        'spotBal': 'spot_bal',
        'spotInUseAmt': 'spot_in_use_amt',
        'spotIsoBal': 'spot_iso_bal',
        'spotUpl': 'spot_upl',
        'spotUplRatio': 'spot_upl_ratio',
        'stgyEq': 'stgy_eq',
        'totalPnl': 'total_pnl',
        'totalPnlRatio': 'total_pnl_ratio',
        'twap': 'twap',
        'uTime': 'u_time',
        'upl': 'upl',
        'uplLiab': 'upl_liab'
    }

    dat = account_api.get_account_balance(**kwargs)['data']
    dat = pd.DataFrame(dat[0]['details'])
    dat['uTime'] = dat.uTime.apply(from_timestamp)
    dat = dat[columns.keys()]
    dat = dat.replace({'': None})
    dat = dat.rename(columns=columns)
    conn.replace_dat(dat=dat, tbl_name='balance')
