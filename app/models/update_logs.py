from sqlalchemy import Column, String, DECIMAL, Integer, DateTime
from app.database.mysql import Base
from app.services.update_strategy import UpdateStrategy


class UpdateLogs(Base):
    __scope__ = 'log'
    __tablename__ = 'update_logs'

    scope = Column(String(255), nullable=True, default='', comment='crypto | bar')
    table = Column(String(255), primary_key=True, nullable=True, default='', comment='表名')
    operation = Column(String(255), nullable=True, default='', comment='更新策略')
    status = Column(Integer, nullable=True, comment='更新状态')
    details = Column(String(2048), nullable=True, default='', comment='失败的话报错信息')
    update_at = Column(DateTime, primary_key=True, nullable=True, comment='更新时间')

    update_strategy = None

    def __repr__(self):
        return f"<Tickets(uid='{self.uid}', datetime='{self.datetime}')>"
