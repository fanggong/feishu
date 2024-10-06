import time
from funcs.const import DEPOSIT_HISTORY
from funcs.utils import *
from database.Mysql import MysqlEngine
from okx.Funding import FundingAPI


def _get_deposit_history(funding_api: FundingAPI, **kwargs):
    dat = funding_api.get_deposit_history(**kwargs).get('data')
    time.sleep(0.2)
    if len(dat) == 0:
        return dat
    else:
        kwargs['after'] = dat[-1]['ts']
        dat = dat + _get_deposit_history(funding_api, **kwargs)
        return dat


def synchronous_deposit_history(conn: MysqlEngine, funding_api=None, **kwargs):
    columns = {
        'actualDepBlkConfirm': 'actual_dep_blk_confirm',
        'amt': 'amt',
        'areaCodeFrom': 'area_code_from',
        'ccy': 'ccy',
        'chain': 'chain',
        'depId': 'dep_id',
        'from': 'from',
        'fromWdId': 'from_wd_id',
        'state': 'state',
        'to': 'to',
        'ts': 'ts',
        'txId': 'tx_id'
    }
    dat = _get_deposit_history(funding_api=funding_api, **kwargs)
    dat = pd.DataFrame(dat)
    dat = dat[columns.keys()]
    dat['ts'] = dat.ts.apply(from_timestamp)
    dat = dat.replace({'': None, '-': None})
    dat = dat.rename(columns=columns)
    conn.upsert_dat(dat=dat, tbl_name=DEPOSIT_HISTORY)


