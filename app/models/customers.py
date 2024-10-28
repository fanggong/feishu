from sqlalchemy import Column, String, DECIMAL, DateTime, Integer
from app.database.mysql import Base
from app.services.update_strategy import UpdateStrategy


class Customers(Base):
    __scope__ = 'bar'
    __tablename__ = 'customers'

    customer_uid = Column(String(255), primary_key=True, nullable=False, default='', comment='客户唯一ID')
    category_name = Column(String(255), nullable=True, default='', comment='分类名称')
    number = Column(String(255), nullable=True, default='', comment='编号')
    name = Column(String(255), nullable=True, default='', comment='名称')
    point = Column(DECIMAL(10, 2), nullable=True, comment='积分')
    discount = Column(DECIMAL(10, 2), nullable=True, comment='折扣')
    balance = Column(DECIMAL(10, 2), nullable=True, comment='余额')
    phone = Column(String(255), nullable=True, default='', comment='电话')
    birthday = Column(String(255), nullable=True, default='', comment='生日')
    qq = Column(String(255), nullable=True, default='', comment='QQ')
    email = Column(String(255), nullable=True, default='', comment='电子邮件')
    address = Column(String(255), nullable=True, default='', comment='地址')
    create_at = Column(DateTime, nullable=True, comment='创建时间')
    update_at = Column(DateTime, nullable=True, comment='更新时间')
    on_account = Column(Integer, nullable=True, comment='挂账')
    enable = Column(Integer, nullable=True, comment='启用')
    sex = Column(Integer, nullable=True, comment='性别')
    total_point = Column(DECIMAL(10, 2), nullable=True, comment='总积分')
    total_ticket_amount = Column(DECIMAL(10, 2), nullable=True, comment='总票据金额')
    total_recharge_amount = Column(DECIMAL(10, 2), nullable=True, comment='总充值金额')
    total_ticket_num = Column(Integer, nullable=True, comment='总票据数量')
    amount_in_arrear = Column(DECIMAL(10, 2), nullable=True, comment='欠款金额')

    update_strategy = UpdateStrategy.FULL

    def __repr__(self):
        return f"<Customers(customer_uid='{self.customer_uid}', name='{self.name}')>"
