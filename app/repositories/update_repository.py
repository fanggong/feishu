import time

from app.database.mysql import db_session
from app.models.update_logs import UpdateLogs
from app.services.update_strategy import UpdateStrategy
from sqlalchemy.dialects.mysql import insert
from datetime import datetime
from app.utils.decorators import retry


class UpdateRepository:
    @staticmethod
    @retry(max_retries=5, delay=1)
    def full_update(table_class, data_list):
        """
        全量更新：删除表中所有数据，插入新数据
        :param table_class: 表对应的 SQLAlchemy ORM 类
        :param data_list: 待插入的数据列表
        """
        session = db_session()
        try:
            with session.begin_nested():
                session.query(table_class).delete()
                for data in data_list:
                    time.sleep(0)
                    new_record = table_class(**data)
                    session.add(new_record)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            db_session.remove()

    @staticmethod
    @retry(max_retries=5, delay=1)
    def incremental_update(table_class, data_list):
        session = db_session()
        try:
            for data in data_list:
                time.sleep(0)
                insert_stmt = insert(table_class).values(**data)
                update_stmt = {key: insert_stmt.inserted[key] for key in data}
                session.execute(insert_stmt.on_duplicate_key_update(**update_stmt))
            session.commit()
        except Exception as e:
            session.rollback()  # 回滚事务
            raise e
        finally:
            db_session.remove()  # 移除会话
