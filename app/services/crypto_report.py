from app.repositories.query_repository import QueryRepository
from app.services.report import ReportService
from app.models.balance import Balance
from app.models.mark_price import MarkPrice
from app.models.positions import Positions
from app.models.instruments import Instruments
from app.models.deposit_history import DepositHistory
from app.models.withdraw_history import WithdrawHistory
from app.models.c2c import C2C
from app.models.update_logs import UpdateLogs
import pandas as pd
import logging

logger = logging.getLogger(__name__)


class CryptoReportService(ReportService):
    id = 'AAq7F02QhXIfo'
    version_name = '1.0.11'

    def report(self):
        logger.info(f'SERVICE IS RUNNING...')
        sql = f'''
            select 
                src.ccy ccy
                ,eq amt
                ,eq * coalesce(mark_px, 1) value
            from (
                select ccy, eq  
                from {Balance.__tablename__} 
            ) src
            left join (
                select 
                    regexp_substr(inst_id, '[A-Z]+', 1, 1) ccy
                    ,mark_px
                from {MarkPrice.__tablename__} 
                where inst_type = 'MARGIN'
                    and regexp_substr(inst_id, '[A-Z]+', 1, 2) = 'USDT'
            ) mp on src.ccy = mp.ccy
            order by value desc
            '''
        spot_asset = QueryRepository.fetch_df_dat(sql)

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
                from {Positions.__tablename__}
            ) src
            left join (
                select 
                    inst_id
                    ,inst_type
                    ,ct_val
                from {Instruments.__tablename__} 
            ) ins on src.inst_id = ins.inst_id and src.inst_type = ins.inst_type
            left join (
                select 
                    regexp_substr(inst_id, '[A-Z]+', 1, 1) ccy
                    ,mark_px
                from {MarkPrice.__tablename__} 
                where inst_type = 'MARGIN'
                    and regexp_substr(inst_id, '[A-Z]+', 1, 2) = 'USDT'
            ) mp on src.ccy = mp.ccy
            order by value desc
            '''
        derivative_asset = QueryRepository.fetch_df_dat(sql)

        sql = f'''
            select 
                src.ccy ccy
                ,upl
                ,upl * coalesce(mark_px, 1) upl_usdt
            from (
                select ccy, upl
                from {Positions.__tablename__} 
            ) src
            left join (
                select 
                    regexp_substr(inst_id, '[A-Z]+', 1, 1) ccy
                    ,mark_px
                from {MarkPrice.__tablename__} 
                where inst_type = 'MARGIN'
                    and regexp_substr(inst_id, '[A-Z]+', 1, 2) = 'USDT'
            ) mp on src.ccy = mp.ccy
            '''
        upl = QueryRepository.fetch_df_dat(sql)

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
                    from {DepositHistory.__tablename__}
                    where state = 2
                    group by ccy
                    union all
                    select 
                        ccy
                        ,0 deposit
                        ,sum(amt) withdraw
                        ,0 c2c_buy
                        ,0 c2c_sell
                    from {WithdrawHistory.__tablename__}
                    where state = 2
                    group by ccy
                    union all
                    select 
                        'USDT' ccy
                        ,0 deposit
                        ,0 withdraw
                        ,sum(if(side = 'buy', amt, 0)) c2c_buy
                        ,sum(if(side = 'sell', amt, 0)) c2c_sell
                    from {C2C.__tablename__}
                ) src
                group by ccy
            ) src
            left join (
                select 
                    regexp_substr(inst_id, '[A-Z]+', 1, 1) ccy
                    ,mark_px
                from {MarkPrice.__tablename__} 
                where inst_type = 'MARGIN'
                    and regexp_substr(inst_id, '[A-Z]+', 1, 2) = 'USDT'
            ) mp on src.ccy = mp.ccy
            '''
        cost = QueryRepository.fetch_df_dat(sql)

        sql = f'''
            select
                src.ccy ccy
                ,imr
                ,imr * coalesce(mark_px, 1) imr_usdt
            from (
                select 
                    ccy
                    ,imr 
                from {Positions.__tablename__}
                where inst_type = 'MARGIN'
            ) src
            left join (
                select 
                    regexp_substr(inst_id, '[A-Z]+', 1, 1) ccy
                    ,mark_px
                from {MarkPrice.__tablename__} 
                where inst_type = 'MARGIN'
                    and regexp_substr(inst_id, '[A-Z]+', 1, 2) = 'USDT'
            ) mp on src.ccy = mp.ccy
            '''
        margin_flow = QueryRepository.fetch_df_dat(sql)

        sql = f'''
            select 
                ccy
                ,margin 
            from {Positions.__tablename__} 
            where inst_type = 'SWAP'
            '''
        contract_flow = QueryRepository.fetch_df_dat(sql)

        sql = f'''
        select max(update_at) update_at
        from {UpdateLogs.__tablename__}
        where status = 1
            and scope = 'crypto'
        '''
        update_at = QueryRepository.fetch_df_dat(sql)
        update_at = update_at.iloc[0, 0].strftime('%Y-%m-%d %H:%M:%S')

        equity = spot_asset.value.sum()
        nav = equity + derivative_asset.value.sum()

        asset_format = pd.concat([spot_asset, derivative_asset]).groupby('ccy').sum().reset_index().sort_values('value', ascending=False)
        asset_format['amt'] = asset_format['amt'].apply(lambda x: self.format_number(x, 6))
        asset_format['value'] = asset_format['value'].apply(lambda x: self.format_number(x, 6))
        asset_format = asset_format.to_dict(orient='records')

        res = {
            'equity': self.format_number(equity, 2),
            'nav': self.format_number(nav, 2),
            'lever': self.format_number(nav / equity, 2),
            'rpnl': self.format_number(equity - cost.amt_usdt.sum() - upl.upl_usdt.sum(), 2),
            'upl': self.format_number(upl.upl_usdt.sum(), 2),
            'pnl': self.format_number(equity - cost.amt_usdt.sum(), 2),
            'contract_flow': self.format_number(contract_flow.margin.sum(), 2),
            'margin_flow': self.format_number(margin_flow.imr_usdt.sum(), 2),
            'free_flow': self.format_number(equity - contract_flow.margin.sum() - margin_flow.imr_usdt.sum(), 2),
            'update_at': update_at,
            'asset': asset_format
        }
        return res