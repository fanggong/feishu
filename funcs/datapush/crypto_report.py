
from database.Mysql import MysqlEngine
from funcs.utils import *
import pandas as pd


def datapush_crypto_report(conn: MysqlEngine):
    sql = f'''
    select 
        src.ccy ccy
        ,eq amt
        ,eq * coalesce(mark_px, 1) value
    from (
        select ccy, eq  
        from balance 
    ) src
    left join (
        select 
            regexp_substr(inst_id, '[A-Z]+', 1, 1) ccy
            ,mark_px
        from mark_price 
        where inst_type = 'MARGIN'
            and regexp_substr(inst_id, '[A-Z]+', 1, 2) = 'USDT'
    ) mp on src.ccy = mp.ccy
    order by value desc
    '''
    asset = conn.fetch_dat(sql)

    sql = f'''
    select 
        src.ccy ccy
        ,pos * coalesce(ct_val, 1) amt
        ,pos * coalesce(ct_val, 1) * mark_px value
    from (
        select
            regexp_substr(inst_id, '[A-Z]+', 1, 1) ccy
            ,inst_id 
            ,inst_type
            ,pos
        from positions
    ) src
    left join (
        select 
            inst_id
            ,inst_type
            ,ct_val
        from instruments i 
    ) ins on src.inst_id = ins.inst_id and src.inst_type = ins.inst_type
    left join (
        select 
            regexp_substr(inst_id, '[A-Z]+', 1, 1) ccy
            ,mark_px
        from mark_price 
        where inst_type = 'MARGIN'
            and regexp_substr(inst_id, '[A-Z]+', 1, 2) = 'USDT'
    ) mp on src.ccy = mp.ccy
    order by value desc
    '''
    derivative_asset = conn.fetch_dat(sql)

    sql = f'''
    select 
        src.ccy ccy
        ,upl
        ,upl * coalesce(mark_px, 1) upl_usdt
    from (
        select ccy, upl
        from positions 
    ) src
    left join (
        select 
            regexp_substr(inst_id, '[A-Z]+', 1, 1) ccy
            ,mark_px
        from mark_price 
        where inst_type = 'MARGIN'
            and regexp_substr(inst_id, '[A-Z]+', 1, 2) = 'USDT'
    ) mp on src.ccy = mp.ccy
    '''
    upl = conn.fetch_dat(sql)

    sql = f'''
    select
        src.ccy ccy
        ,amt
        ,amt * coalesce(mark_px, 1) amt_usdt
    from (
        select 
            ccy
            ,sum(deposit) deposit
            ,sum(withdraw) withdraw
            ,sum(c2c_buy) c2c_buy
            ,sum(c2c_sell) c2c_sell
            ,sum(c2c_buy) - sum(c2c_sell) + sum(deposit) - sum(withdraw) amt
        from (
            select 
                ccy
                ,sum(amt) deposit
                ,0 withdraw
                ,0 c2c_buy
                ,0 c2c_sell
            from deposit_history
            where state = 2
            group by ccy
            union all
            select 
                ccy
                ,0 deposit
                ,sum(amt) withdraw
                ,0 c2c_buy
                ,0 c2c_sell
            from withdraw_history
            where state = 2
            group by ccy
            union all
            select 
                'USDT' ccy
                ,0 deposit
                ,0 withdraw
                ,sum(if(side = 'buy', amt, 0)) c2c_buy
                ,sum(if(side = 'sell', amt, 0)) c2c_sell
            from c2c
        ) src
        group by ccy
    ) src
    left join (
        select 
            regexp_substr(inst_id, '[A-Z]+', 1, 1) ccy
            ,mark_px
        from mark_price 
        where inst_type = 'MARGIN'
            and regexp_substr(inst_id, '[A-Z]+', 1, 2) = 'USDT'
    ) mp on src.ccy = mp.ccy
    '''
    cost = conn.fetch_dat(sql)

    sql = f'''
    select
        src.ccy ccy
        ,imr
        ,imr * coalesce(mark_px, 1) imr_usdt
    from (
        select 
            ccy
            ,imr 
        from positions
        where inst_type = 'MARGIN'
    ) src
    left join (
        select 
            regexp_substr(inst_id, '[A-Z]+', 1, 1) ccy
            ,mark_px
        from mark_price 
        where inst_type = 'MARGIN'
            and regexp_substr(inst_id, '[A-Z]+', 1, 2) = 'USDT'
    ) mp on src.ccy = mp.ccy
    '''
    margin_flow = conn.fetch_dat(sql)

    sql = f'''
    select 
        ccy
        ,margin 
    from positions p 
    where inst_type = 'SWAP'
    '''
    contract_flow = conn.fetch_dat(sql)

    sql = f'''
    select max(update_at) update_at
    from update_log
    '''
    update_at = conn.fetch_dat(sql).update_at[0].strftime('%Y-%m-%d %H:%M:%S')

    total_asset = asset.value.sum()
    position_asset = total_asset + derivative_asset.value.sum()

    asset_format = pd.concat([asset, derivative_asset]).groupby('ccy').sum().reset_index().sort_values('value', ascending=False)
    asset_format['amt'] = asset_format['amt'].apply(lambda x: format_number(x, 6))
    asset_format['value'] = asset_format['value'].apply(lambda x: format_number(x, 6))
    asset_format = asset_format.to_dict(orient='records')

    res = {
        'total_asset': format_number(total_asset, 2),
        'position_asset': format_number(position_asset, 2),
        'liability_ratio': format_number(position_asset / total_asset, 2),
        'rpnl': format_number(total_asset - cost.amt_usdt.sum() - upl.upl_usdt.sum(), 2),
        'upl': format_number(upl.upl_usdt.sum(), 2),
        'pnl': format_number(total_asset - cost.amt_usdt.sum(), 2),
        'contract_flow': format_number(contract_flow.margin.sum(), 2),
        'margin_flow': format_number(margin_flow.imr_usdt.sum(), 2),
        'free_flow': format_number(total_asset - contract_flow.margin.sum() - margin_flow.imr_usdt.sum(), 2),
        'update_at': update_at,
        'asset': asset_format
    }
    return res


# def datapush_risk_report(conn: MysqlEngine):
#     sql =