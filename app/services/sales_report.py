from app.services.report import ReportService
from app.repositories.query_repository import QueryRepository
from datetime import datetime, timedelta
from app.models.calendar import Calendar
from app.models.tickets import Tickets
from app.models.ticket_items import TicketItems
from app.models.update_logs import UpdateLogs


class SalesReportService(ReportService):
    id = 'AAq72IXC2cGmT'
    version_name = '1.0.3'

    def report(self):
        sql = f'''
        select
            sum(if(date(datetime) = current_date - interval 1 day, total_amount, 0)) revenue_prior
            ,sum(if(date(datetime) = current_date - interval 1 day, 1, 0)) customers_prior
            ,sum(if(date(datetime) between current_date - interval weekday(current_date - interval 1 day) + 1 day and current_date - interval 1 day, total_amount, 0)) revenue_wtd
            ,sum(if(date(datetime) between current_date - interval weekday(current_date - interval 1 day) + 1 day and current_date - interval 1 day, 1, 0)) customers_wtd
            ,sum(if(date(datetime) between date_format(current_date - interval 1 day, '%Y-%m-01') and current_date - interval 1 day, total_amount, 0)) revenue_mtd
            ,sum(if(date(datetime) between date_format(current_date - interval 1 day, '%Y-%m-01') and current_date - interval 1 day, 1, 0)) customers_mtd
            ,sum(if(date(datetime) between current_date - interval weekday(current_date - interval 1 day) + 7 day and current_date - interval weekday(current_date) day, total_amount, 0)) revenue_pre_week
            ,sum(if(date(datetime) between current_date - interval weekday(current_date - interval 1 day) + 7 day and current_date - interval weekday(current_date) day, 1, 0)) customers_pre_week
            ,sum(if(date(datetime) between date_format(current_date - interval day(current_date - interval 1 day) + 1 day, '%Y-%m-01') and date_format(current_date - interval 1 day, '%Y-%m-01') - interval 1 day, total_amount, 0)) revenue_pre_month
            ,sum(if(date(datetime) between date_format(current_date - interval day(current_date - interval 1 day) + 1 day, '%Y-%m-01') and date_format(current_date - interval 1 day, '%Y-%m-01') - interval 1 day, 1, 0)) customers_pre_month
        from {Tickets.__tablename__}
        where date(datetime) between date_format(current_date - interval day(current_date) + 1 day, '%Y-%m-01') and current_date - interval 1 day
            and invalid = 0
        '''
        sales = QueryRepository.fetch_df_dat(sql).iloc[0, :].to_dict()
        sales['atv_prior'] = 0 if sales['customers_prior'] == 0 else sales['revenue_prior'] / sales['customers_prior']
        sales['atv_wtd'] = 0 if sales['customers_wtd'] == 0 else sales['revenue_wtd'] / sales['customers_wtd']
        sales['atv_mtd'] = 0 if sales['customers_mtd'] == 0 else sales['revenue_mtd'] / sales['customers_mtd']
        sales['atv_pre_week'] = 0 if sales['customers_pre_week'] == 0 else sales['revenue_pre_week'] / sales['customers_pre_week']
        sales['atv_pre_month'] = 0 if sales['customers_pre_month'] == 0 else sales['revenue_pre_month'] / sales['customers_pre_month']

        sql = f'''
        select 
            name
            ,sum(quantity) quantity
            ,sum(total_amount) amount
        from {TicketItems.__tablename__}
        where ticket_uid in (
            select uid
            from {Tickets.__tablename__}
            where date(datetime) = current_date - interval 1 day
                and invalid = 0
        )
        group by name
        order by amount desc
        '''
        item_day = QueryRepository.fetch_df_dat(sql)
        item_day = self.process_item(item_day)

        sql = f'''
        select 
            name
            ,sum(quantity) quantity
            ,sum(total_amount) amount
        from {TicketItems.__tablename__}
        where ticket_uid in (
            select uid
            from {Tickets.__tablename__}
            where date(datetime) between current_date - interval weekday(current_date - interval 1 day) + 1 day and current_date - interval 1 day
                and invalid = 0
        )
        group by name
        order by amount desc
        '''
        item_week = QueryRepository.fetch_df_dat(sql)
        item_week = self.process_item(item_week)

        sql = f'''
        select 
            name
            ,sum(quantity) quantity
            ,sum(total_amount) amount
        from {TicketItems.__tablename__}
        where ticket_uid in (
            select uid
            from {Tickets.__tablename__}
            where date(datetime) between date_format(current_date - interval 1 day, '%Y-%m-01') and current_date - interval 1 day
                and invalid = 0
        )
        group by name
        order by amount desc
        '''
        item_month = QueryRepository.fetch_df_dat(sql)
        item_month = self.process_item(item_month)

        sql = f'''
        select max(update_at) update_at
        from {UpdateLogs.__tablename__}
        where scope = 'bar'
        '''
        update_at = QueryRepository.fetch_df_dat(sql).iloc[0, 0].strftime('%Y-%m-%d %H:%M:%S')

        res = {
            'update_at': update_at,
            'revenue_prior': self.format_number(sales['revenue_prior'], 2),
            'customers_prior': self.format_number(sales['customers_prior'], 0),
            'atv_prior': self.format_number(sales['atv_prior'], 2),
            'revenue_wtd': self.format_number(sales['revenue_wtd'], 2),
            'customers_wtd': self.format_number(sales['customers_wtd'], 0),
            'atv_wtd': self.format_number(sales['atv_wtd'], 2),
            'revenue_mtd': self.format_number(sales['revenue_mtd'], 2),
            'customers_mtd': self.format_number(sales['customers_mtd'], 0),
            'atv_mtd': self.format_number(sales['atv_mtd'], 2),
            'revenue_pre_week': self.format_number(sales['revenue_pre_week'], 2),
            'customers_pre_week': self.format_number(sales['customers_pre_week'], 0),
            'revenue_pre_month': self.format_number(sales['revenue_pre_month'], 2),
            'customers_pre_month': self.format_number(sales['customers_pre_month'], 0),
            'item_day': item_day,
            'item_week': item_week,
            'item_month': item_month
        }
        return res

    def process_item(self, item):
        item['quantity'] = item['quantity'].apply(self.format_number, decimals=0)
        item['amount'] = item['amount'].apply(self.format_number, decimals=2)
        item = item.to_dict(orient='records')
        return item