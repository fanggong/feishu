from sqlalchemy import Column, String, DECIMAL, Integer, DateTime
from app.database.mysql import Base
from app.services.update_strategy import UpdateStrategy


class Tickets(Base):
    __scope__ = 'bar'
    __tablename__ = 'tickets'

    cashier_uid = Column(String(255), nullable=True, default='', comment='收银员唯一 ID')
    customer_uid = Column(String(255), nullable=True, default='', comment='客户唯一 ID')
    uid = Column(String(255), primary_key=True, nullable=False, default='', comment='票据唯一 ID')
    sn = Column(String(255), nullable=True, default='', comment='序列号')
    datetime = Column(DateTime, nullable=True, comment='日期时间')
    total_amount = Column(DECIMAL(10, 2), nullable=True, comment='总金额')
    total_profit = Column(DECIMAL(10, 2), nullable=True, comment='总利润')
    discount = Column(DECIMAL(10, 2), nullable=True, comment='折扣')
    rounding = Column(DECIMAL(10, 2), nullable=True, comment='四舍五入')
    ticket_type = Column(String(255), nullable=True, default='', comment='票据类型')
    invalid = Column(Integer, nullable=True, comment='是否无效')
    sys_update_time = Column(DateTime, nullable=True, comment='系统更新时间')
    remark = Column(String(255), nullable=True, default='', comment='备注')
    service_fee = Column(DECIMAL(10, 2), nullable=True, comment='服务费')
    coupon_fee = Column(DECIMAL(10, 2), nullable=True, comment='优惠券费用')
    job_number = Column(String(255), nullable=True, default='', comment='工号')
    name = Column(String(255), nullable=True, default='', comment='名称')
    code = Column(String(255), nullable=True, default='', comment='代码')
    amount = Column(DECIMAL(10, 2), nullable=True, comment='金额')

    update_strategy = UpdateStrategy.INCREMENTAL

    def __repr__(self):
        return f"<Tickets(uid='{self.uid}', datetime='{self.datetime}')>"
