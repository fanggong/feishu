from airflow.decorators import task, dag
from airflow.models import Variable
import logging
import pendulum

cfg = Variable.get('okx', deserialize_json=True)

logger = logging.getLogger(__name__)
default_args = {
    'owner': 'Fang Yongchao'
}


def generate_sql_template(schema, table, type):
    import pandas as pd
    from include.database.mysql import engine
    primary_key = pd.read_sql(
        f"select column_name from information_schema.columns where table_schema = '{schema}' and table_name = '{table}' and column_key = 'PRI'", engine
    )
    primary_key = primary_key['COLUMN_NAME'].to_list()
    other_columns = pd.read_sql(
        f"select column_name from information_schema.columns where table_schema = '{schema}' and table_name = '{table}' and column_key != 'PRI'", engine
    )
    other_columns = other_columns['COLUMN_NAME'].to_list()
    
    sql = []
    if type == 'insert':
        sql.append(f'delete from {schema}.{table} where 1 = 1;')
        sql.append(f'''
        insert into {schema}.{table} ({','.join(primary_key + other_columns)})
        values ({','.join([f':{each}' for each in primary_key + other_columns])});
        ''')
    elif type == 'upsert':
        sql.append(f'''
        insert into {schema}.{table} ({','.join(primary_key + other_columns)})
        values ({','.join([f':{each}' for each in primary_key + other_columns])})
        on duplicate key update
        {',\n'.join([f'{each} = values({each})' for each in other_columns])};
        ''')
    return sql


@dag(schedule='0 */24 * * *', start_date=pendulum.datetime(2025, 1, 25), catchup=True, 
     default_args=default_args)
def manual():
    @task
    def bills_history(**kwargs):
        from include.services.bills_history_fetcher import BillsHistoryFetcher
        from include.database.mysql import engine
        from sqlalchemy import text
        schema = 'crypto'
        table = 'bills_history'
        type = 'upsert'
        begin = int(kwargs['data_interval_start'].timestamp()*1000)
        end = int(kwargs['data_interval_end'].timestamp()*1000)
        data = BillsHistoryFetcher(**cfg).fetch_data(begin=begin, end=end)
        logger.info(f'{schema}.{table} 更新数据 {len(data)} items')
        if data:
            sql = generate_sql_template(schema, table, type)
            for each in sql:
                with engine.connect() as conn:
                    conn.execute(text(each), data)

    bills_history()

manual()