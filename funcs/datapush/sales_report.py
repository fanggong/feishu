import json

from database.Mysql import MysqlEngine
from funcs.utils import *
from funcs.const import *


def datapush_sales_report(conn: MysqlEngine, start_date=None, end_date=None):
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
        from {CALENDAR}
        where date between '{start_date}' and '{end_date}'
    ) src
    left join (
        select 
            date(datetime - interval 4 hour) order_date
            ,sum(total_amount) sales
            ,count(uid) order_number
            ,sum(total_amount) / count(uid) atv
        from {TICKETS}
        where invalid = 0
            and date(datetime - interval 4 hour) between '{start_date}' and '{end_date}'
        group by date(datetime - interval 4 hour)
        order by order_date asc
    ) tck on src.date = tck.order_date
    '''
    dat = conn.fetch_dat(sql)
    dat['order_date'] = dat['order_date'].apply(str)
    graph_sales = {
        'type': 'bar',
        'title': {
            'text': 'Sales'
        },
        'data': {
            'values': dat[['order_date', 'sales']].to_dict(orient='records')
        },
        'xField': 'order_date',
        'yField': 'sales',
        'axes': [
            {
                'orient': 'bottom',
                'label': {
                    'autoRotate': False
                }
            }
        ]
    }

    graph_number = {
        'type': 'bar',
        'title': {
            'text': 'Order Size'
        },
        'data': {
            'values': dat[['order_date', 'order_number']].to_dict(orient='records')
        },
        'xField': 'order_date',
        'yField': 'order_number',
        'axes': [
            {
                'orient': 'bottom',
                'label': {
                    'autoRotate': False
                }
            }
        ]
    }

    graph_atv = {
        'type': 'bar',
        'title': {
            'text': 'ATV'
        },
        'data': {
            'values': dat[['order_date', 'atv']].to_dict(orient='records')
        },
        'xField': 'order_date',
        'yField': 'atv',
        'axes': [
            {
                'orient': 'bottom',
                'label': {
                    'autoRotate': False
                }
            }
        ]
    }

    sql = f'''
    select max(update_at) update_at
    from update_log
    where role = 'BC'
    '''
    update_at = conn.fetch_dat(sql).update_at[0].strftime('%Y-%m-%d %H:%M:%S')

    res = {
        'start_date': start_date,
        'end_date': end_date,
        'graph_sales': graph_sales,
        'graph_number': graph_number,
        'graph_atv': graph_atv,
        'update_at': update_at
    }
    return res