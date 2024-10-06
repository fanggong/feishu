from funcs.const import MARK_PRICE
from funcs.utils import *
from database.Mysql import MysqlEngine
from okx.PublicData import PublicAPI


def synchronous_mark_price(conn: MysqlEngine, public_api: PublicAPI, inst_type, **kwargs):
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
    conn.upsert_dat(dat=dat, tbl_name=MARK_PRICE)