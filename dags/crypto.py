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


@dag(schedule='0 */2 * * *', start_date=pendulum.datetime(2023, 1, 1), catchup=False, 
     default_args=default_args)
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
        logger.info(f'{schema}.{table} 更新数据 {len(data)} items')
        for each in sql:
            with engine.connect() as conn:
                conn.execute(text(each), data)
    
    @task
    def deposit_history():
        from include.services.deposit_history_fetcher import DepositHistoryFetcher
        from include.database.mysql import engine
        from sqlalchemy import text
        schema = 'crypto'
        table = 'deposit_history'
        type = 'insert'
        data = DepositHistoryFetcher(**cfg).fetch_data()
        sql = generate_sql_template(schema, table, type)
        logger.info(f'{schema}.{table} 更新数据 {len(data)} items')
        for each in sql:
            with engine.connect() as conn:
                conn.execute(text(each), data)
    
    @task
    def withdraw_history():
        from include.services.withdraw_history_fetcher import WithdrawHistoryFetcher
        from include.database.mysql import engine
        from sqlalchemy import text
        schema = 'crypto'
        table = 'withdraw_history'
        type = 'insert'
        data = WithdrawHistoryFetcher(**cfg).fetch_data()
        sql = generate_sql_template(schema, table, type)
        logger.info(f'{schema}.{table} 更新数据 {len(data)} items')
        for each in sql:
            with engine.connect() as conn:
                conn.execute(text(each), data)

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

    @task
    def instruments():
        from include.services.instruments_fetcher import InstrumentsFetcher
        from include.database.mysql import engine
        from sqlalchemy import text
        schema = 'crypto'
        table = 'instruments'
        type = 'upsert'
        inst_type_list = ['SPOT', 'MARGIN', 'SWAP']
        for inst_type in inst_type_list:
            data = InstrumentsFetcher(**cfg).fetch_data(instType=inst_type)
            logger.info(f'{schema}.{table} inst_type = {inst_type} 更新数据 {len(data)} items')
            if data:
                sql = generate_sql_template(schema, table, type)
                for each in sql:
                    with engine.connect() as conn:
                        conn.execute(text(each), data)

    @task
    def mark_price(**kwargs):
        from include.services.mark_price_fetcher import MarkPriceFetcher
        from include.database.mysql import engine
        from sqlalchemy import text
        schema = 'crypto'
        table = 'mark_price'
        type = 'upsert'
        inst_type_list = ['MARGIN', 'SWAP']
        for inst_type in inst_type_list:
            data = MarkPriceFetcher(**cfg).fetch_data(instType=inst_type)
            logger.info(f'{schema}.{table} inst_type = {inst_type} 更新数据 {len(data)} items')
            if data:
                sql = generate_sql_template(schema, table, type)
                for each in sql:
                    with engine.connect() as conn:
                        conn.execute(text(each), data)

    mark_price() >> instruments() >> bills_history() >> balance() >> deposit_history() >> withdraw_history()

crypto()