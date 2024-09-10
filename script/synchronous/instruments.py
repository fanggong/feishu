import pandas as pd
from script.utils import *


def synchronous_instruments(conn, public_api, **kwargs):
    columns = {
        'alias': 'alias',
        'baseCcy': 'base_ccy',
        'category': 'category',
        'ctMult': 'ct_mult',
        'ctType': 'ct_type',
        'ctVal': 'ct_val',
        'ctValCcy': 'ct_val_ccy',
        'expTime': 'exp_time',
        'instFamily': 'inst_family',
        'instId': 'inst_id',
        'instType': 'inst_type',
        'lever': 'level',
        'listTime': 'list_time',
        'lotSz': 'lot_sz',
        'maxIcebergSz': 'max_iceberg_sz',
        'maxLmtAmt': 'max_lmt_amt',
        'maxLmtSz': 'max_lmt_sz',
        'maxMktAmt': 'max_mkt_amt',
        'maxMktSz': 'max_mkt_sz',
        'maxStopSz': 'max_stop_sz',
        'maxTriggerSz': 'max_trigger_sz',
        'maxTwapSz': 'max_twap_sz',
        'minSz': 'min_sz',
        'optType': 'opt_type',
        'quoteCcy': 'quote_ccy',
        'ruleType': 'rule_type',
        'settleCcy': 'settle_ccy',
        'state': 'state',
        'stk': 'stk',
        'tickSz': 'tick_sz',
        'uly': 'uly'
    }
    dat = public_api.get_instruments(**kwargs)['data']
    dat = pd.DataFrame(dat)
    dat['expTime'] = dat.expTime.apply(from_timestamp)
    dat['listTime'] = dat.listTime.apply(from_timestamp)
    dat = dat[columns.keys()]
    dat = dat.replace({'': None})
    dat = dat.rename(columns=columns)
    conn.upsert_dat(dat=dat, tbl_name='instruments')