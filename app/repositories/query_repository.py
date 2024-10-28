from sqlalchemy import text
from app.database.mysql import db_session
import pandas as pd


class QueryRepository:
    @staticmethod
    def execute_raw_sql(sql: str, params=None):
        """
        执行一段原生 SQL 查询，并返回结果
        :param sql: 要执行的 SQL 语句
        :param params: 可选的 SQL 参数
        :return: 查询结果
        """
        session = db_session()
        try:
            result = session.execute(text(sql), params)
            return result.fetchall()
        finally:
            session.close()

    @staticmethod
    def fetch_df_dat(sql: str, params=None):
        """
        使用 session 执行原生 SQL 查询，并返回结果的 DataFrame
        :param sql: 要执行的 SQL 语句
        :param params: 可选的 SQL 参数
        :return: 查询结果的 DataFrame
        """
        # 通过Session获取数据库连接
        session = db_session()
        try:
            # 获取数据库连接
            connection = session.connection()
            # 使用 pandas 的 read_sql 来执行查询
            return pd.read_sql(text(sql), con=connection, params=params)
        finally:
            session.close()
