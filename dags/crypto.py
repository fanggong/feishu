from airflow.decorators import task, dag
from airflow.models import Variable
import logging
import pendulum

cfg = Variable.get('okx', deserialize_json=True)

logger = logging.getLogger(__name__)
default_args = {
    'owner': 'Fang Yongchao'
}
MYSQL_KEYWORDS = []

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

    primary_key = [f'{each}_s' if each in MYSQL_KEYWORDS else each for each in primary_key]
    other_columns = [f'`{each}`' if each in MYSQL_KEYWORDS else each for each in other_columns]

    if type == 'insert':
        sql = f'''
        delete from {schema}.{table} where 1 = 1;
        insert into {schema}.{table} ({','.join(primary_key + other_columns)})
        values ({','.join([f':{each}' for each in primary_key + other_columns])});
        '''
    elif type == 'upsert':
        sql = f'''
        insert into {schema}.{table} ({','.join(primary_key + other_columns)})
        values ({','.join([f':{each}' for each in primary_key + other_columns])})
        on duplicate key update
        {',\n'.join([f'{each} = if(values(update_time) >= update_time or update_time is null, values({each}), {each})' for each in other_columns])}
        '''
    return sql


@dag(schedule=None, default_args=default_args)
def crypto():
    @task
    def balance():
        from include.services.balance_fetcher import BalanceFetcher
        from include.database.mysql import engine
        from sqlalchemy import text
        schema = 'crypto'
        table = 'balance'
        type = 'insert'
        data = BalanceFetcher(**cfg).fetch_data()
        sql = generate_sql_template(schema, table, type)
        logger.info(sql)
        logger.info(f'更新数据 {len(data)} items')
        with engine.connect() as conn:
            conn.execute(text(sql), data)
        return data
    
    @task
    def bills_history():
        pass
    
    balance()

crypto()