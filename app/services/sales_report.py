from app.services.report import ReportService
from app.repositories.query_repository import QueryRepository
from datetime import datetime, timedelta
from app.models.calendar import Calendar
from app.models.tickets import Tickets
from app.models.update_logs import UpdateLogs


class SalesReportService(ReportService):
    id = 'AAq7QaZZ15OqP'
    version_name = '1.0.15'

    def report(self, start_date=None, end_date=None):
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d') if not start_date else start_date
        end_date = datetime.now().strftime('%Y-%m-%d') if not end_date else end_date

        sql = f'''
            select 
                src.date order_date
                ,coalesce(sales, 0) sales
                ,coalesce(order_number, 0) order_number
                ,round(coalesce(atv, 0), 2) atv
            from (
                select date
                from {Calendar.__tablename__}
                where date between '{start_date}' and '{end_date}'
            ) src
            left join (
                select 
                    date(datetime - interval 4 hour) order_date
                    ,sum(total_amount) sales
                    ,count(uid) order_number
                    ,sum(total_amount) / count(uid) atv
                from {Tickets.__tablename__}
                where invalid = 0
                    and date(datetime - interval 4 hour) between '{start_date}' and '{end_date}'
                group by date(datetime - interval 4 hour)
                order by order_date asc
            ) tck on src.date = tck.order_date
            '''
        dat = QueryRepository.fetch_df_dat(sql)
        dat['order_date'] = dat['order_date'].apply(str)
        graph_sales = {
            'type': 'bar',
            'title': {
                'text': 'Sales'
            },
            'data': {
                'values': dat[['order_date', 'sales']].to_dict(orient='records')
            },
            'direction': 'horizontal',
            'xField': 'sales',
            'yField': 'order_date',
            'axes': [
                {
                    'orient': 'bottom',
                    'title': 'Sales Amount',
                    'grid': True
                },
                {
                    'orient': 'left',
                    'title': 'Time',
                    'grid': True,
                    'label': {
                        'align': 'left'  # 将 Y 轴的标签左对齐
                    }
                }
            ],
            'label': {
                'position': 'inside',
                'smartInvert': False
            },
            'bar': {
                'barWidth': 20,  # 柱子的宽度
                'cornerRadius': [4, 4, 0, 0]  # 柱子的圆角
            }
        }


        sql = f'''
        select max(update_at) update_at
        from {UpdateLogs.__tablename__}
        where scope = 'bar'
        '''
        update_at = QueryRepository.fetch_df_dat(sql).iloc[0, 0].strftime('%Y-%m-%d %H:%M:%S')

        res = {
            'start_date': start_date,
            'end_date': end_date,
            'graph_sales': graph_sales,
            'update_at': update_at
        }
        return res