

from database.Mysql import MysqlEngine
from funcs.utils import *
import pandas as pd


def datapush_risk_report(conn: MysqlEngine):
    sql = f'''
    select 
        concat(regexp_substr(src.inst_id, '[A-Z]+', 1, 1), '(', lever, ')') ccy
        ,margin + upl margin
        ,(avg_px * pos * ct_val / lever * (lever - 1)) / (avg_px * pos * ct_val / lever * (lever - 1) + margin + upl) * 100 liability_ratio
    from (
        select
            inst_id
            ,margin
            ,upl
            ,avg_px 
            ,pos
            ,round(lever, 0)  lever
        from positions p 
        where inst_type = 'SWAP'
    ) src
    left join (
        select inst_id, ct_val
        from instruments
    ) ins on src.inst_id = ins.inst_id 
    order by margin desc
    '''
    contract = conn.fetch_dat(sql)
    contract['margin'] = contract['margin'].apply(lambda x: format_number(x, 4))
    contract['liability_ratio'] = contract['liability_ratio'].apply(lambda x: format_number(x, 2) + '%')

    sql = f'''
    select 
        concat(src.ccy, '(', lever, ')') ccy
        ,eq * mark_px margin
        ,liab / (liab + eq * mark_px) * 100 liability_ratio
    from (
        select
            regexp_substr(inst_id, '[A-Z]+', 1, 1) ccy
            ,-liab liab
            ,round(lever, 0) lever
        from positions p 
        where inst_type = 'MARGIN'
    ) src
    left join (
        select ccy, eq
        from balance
    ) bal on src.ccy = bal.ccy
    left join (
        select 
            regexp_substr(inst_id, '[A-Z]+', 1, 1) ccy
            ,mark_px
        from mark_price 
        where inst_type = 'MARGIN'
            and regexp_substr(inst_id, '[A-Z]+', 1, 2) = 'USDT'
    ) mp on src.ccy = mp.ccy
    order by margin desc
    '''
    margin = conn.fetch_dat(sql)
    margin['margin'] = margin['margin'].apply(lambda x: format_number(x, 4))
    margin['liability_ratio'] = margin['liability_ratio'].apply(lambda x: format_number(x, 2) + '%')

    sql = f'''
    select max(update_at) update_at
    from update_log
    '''
    update_at = conn.fetch_dat(sql).update_at[0].strftime('%Y-%m-%d %H:%M:%S')

    res = {
        'contract': contract.to_dict(orient='records'),
        'margin': margin.to_dict(orient='records'),
        'update_at': update_at
    }
    return res