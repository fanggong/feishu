from sqlalchemy import create_engine, text, MetaData, Table
from sqlalchemy.dialects.mysql import insert
from .utils import *

import pandas as pd
import numpy as np


class MysqlEngine:
    def __init__(self, user_name, password, host, port=29307, database='xlsd', **kwargs):
        url = f'mysql+pymysql://{user_name}:{password}@{host}:{port}/{database}'
        self.engine = create_engine(url, connect_args={'connect_timeout': 10}, **kwargs)

    @retry(max_retries=3, delay=1)
    def run_sql(self, sql, params=None):
        with self.engine.connect() as conn:
            conn.execute(text(sql), params)

    @retry(max_retries=3, delay=1)
    def fetch_dat(self, sql):
        return pd.read_sql(sql, self.engine)

    @retry(max_retries=3, delay=1)
    def append_dat(self, dat, tbl_name, index, schema):
        dat.to_sql(tbl_name, self.engine, if_exists='append', index=index, schema=schema)

    @retry(max_retries=3, delay=1)
    def replace_dat(self, dat, tbl_name, index=False, schema=None):
        if schema:
            self.run_sql(f'truncate table {schema}.{tbl_name}')
        else:
            self.run_sql(f'truncate table {tbl_name}')
        dat.to_sql(tbl_name, self.engine, if_exists='append', index=index, schema=schema)

    @retry(max_retries=3, delay=1)
    def upsert_dat(self, dat, tbl_name):
        table = Table(tbl_name, MetaData(), autoload_with=self.engine)
        data_dict = dat.replace({np.nan: None}).to_dict(orient='records')
        insert_stmt = insert(table).values(data_dict)
        update_dict = {c.name: insert_stmt.inserted[c.name] for c in table.columns if c.name in dat.columns}
        upsert_stmt = insert_stmt.on_duplicate_key_update(update_dict)
        with self.engine.connect() as conn:
            conn.execute(upsert_stmt)
            conn.commit()

    def __del__(self):
        self.engine.dispose()
