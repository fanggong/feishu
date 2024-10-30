from app.database.mysql import db_session
from app.models.update_logs import UpdateLogs
from app.services.update_strategy import UpdateStrategy
from sqlalchemy.dialects.mysql import insert
from datetime import datetime
from app.utils.decorators import retry


class UpdateRepository:
    @staticmethod
    @retry(max_retries=3, delay=2, exceptions=(TimeoutError, ConnectionError))
    def full_update(table_class, data_list):
        """
        全量更新：删除表中所有数据，插入新数据
        :param table_class: 表对应的 SQLAlchemy ORM 类
        :param data_list: 待插入的数据列表
        """
        session = db_session()
        try:
            # 删除表中所有数据
            session.query(table_class).delete()
            session.commit()

            # 插入新数据
            for data in data_list:
                new_record = table_class(**data)
                session.add(new_record)
            session.commit()
        except Exception as e:
            session.rollback()  # 回滚事务
            raise e
        finally:
            db_session.remove()  # 移除会话

    @staticmethod
    @retry(max_retries=3, delay=2, exceptions=(TimeoutError, ConnectionError))
    def incremental_update(table_class, data_list):
        """
        增量更新：根据主键来判断，存在则更新，不存在则插入
        :param table_class: 表对应的 SQLAlchemy ORM 类
        :param data_list: 待更新的数据列表
        """
        session = db_session()
        try:
            for data in data_list:
                # 使用 SQLAlchemy 提供的 insert 构造
                insert_stmt = insert(table_class).values(**data)

                # 构造 ON DUPLICATE KEY UPDATE 部分
                update_stmt = {key: insert_stmt.inserted[key] for key in data}

                # 执行插入或更新
                session.execute(insert_stmt.on_duplicate_key_update(**update_stmt))
            session.commit()
        except Exception as e:
            session.rollback()  # 回滚事务
            raise e
        finally:
            db_session.remove()  # 移除会话
