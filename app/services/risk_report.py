from app.services.report import ReportService
from app.models.positions import Positions
from app.models.instruments import Instruments
from app.models.balance import Balance
from app.models.mark_price import MarkPrice
from app.models.update_logs import UpdateLogs
from app.repositories.query_repository import QueryRepository


class RiskReportService(ReportService):
    id = 'AAq7xvyDvK3WX'
    version_name = '1.0.3'

    def report(self):
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
                from {Positions.__tablename__} 
                where inst_type = 'SWAP'
            ) src
            left join (
                select inst_id, ct_val
                from {Instruments.__tablename__}
            ) ins on src.inst_id = ins.inst_id 
            order by margin desc
            '''
        contract = QueryRepository.fetch_df_dat(sql)
        contract['margin'] = contract['margin'].apply(lambda x: self.format_number(x, 4))
        contract['liability_ratio'] = contract['liability_ratio'].apply(lambda x: self.format_number(x, 2) + '%')

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
                from {Positions.__tablename__}
                where inst_type = 'MARGIN'
            ) src
            left join (
                select ccy, eq
                from {Balance.__tablename__}
            ) bal on src.ccy = bal.ccy
            left join (
                select 
                    regexp_substr(inst_id, '[A-Z]+', 1, 1) ccy
                    ,mark_px
                from {MarkPrice.__tablename__} 
                where inst_type = 'MARGIN'
                    and regexp_substr(inst_id, '[A-Z]+', 1, 2) = 'USDT'
            ) mp on src.ccy = mp.ccy
            order by margin desc
            '''
        margin = QueryRepository.fetch_df_dat(sql)
        margin['margin'] = margin['margin'].apply(lambda x: self.format_number(x, 4))
        margin['liability_ratio'] = margin['liability_ratio'].apply(lambda x: self.format_number(x, 2) + '%')

        sql = f'''
            select max(update_at) update_at
            from {UpdateLogs.__tablename__}
            where role = 'bar'
            '''
        update_at = QueryRepository.fetch_df_dat(sql).iloc[0, 0].strftime('%Y-%m-%d %H:%M:%S')

        res = {
            'contract': contract.to_dict(orient='records'),
            'margin': margin.to_dict(orient='records'),
            'update_at': update_at
        }
        return res