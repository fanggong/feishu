from app.database.mysql import db_session
from app.models.update_logs import UpdateLogs
from app.services.update_strategy import UpdateStrategy
from sqlalchemy import insert
from datetime import datetime


class UpdateRepository:
    @staticmethod
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
    def incremental_update(table_class, data_list):
        """
        增量更新：根据主键来判断，存在则更新，不存在则插入
        :param table_class: 表对应的 SQLAlchemy ORM 类
        :param data_list: 待更新的数据列表
        """
        session = db_session()
        try:
            primary_key_columns = [key.name for key in table_class.__mapper__.primary_key]

            for data in data_list:
                # 创建过滤条件
                primary_key_filter = {key: data[key] for key in primary_key_columns}
                existing_record = session.query(table_class).filter_by(**primary_key_filter).first()

                if existing_record:
                    # 如果记录存在，更新所有字段
                    for key, value in data.items():
                        setattr(existing_record, key, value)
                else:
                    # 如果记录不存在，则插入新记录
                    new_record = table_class(**data)
                    session.add(new_record)
            session.commit()
        except Exception as e:
            session.rollback()  # 回滚事务
            raise e
        finally:
            db_session.remove()  # 移除会话
