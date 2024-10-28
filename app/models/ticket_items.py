from sqlalchemy import Column, String, DECIMAL, Integer
from app.database.mysql import Base
from app.services.update_strategy import UpdateStrategy


class TicketItems(Base):
    __scope__ = 'bar'
    __tablename__ = 'ticket_items'

    ticket_uid = Column(String(255), primary_key=True, nullable=False, default='', comment='票据唯一 ID')
    id = Column(String(255), primary_key=True, nullable=False, default='', comment='项目 ID')
    name = Column(String(255), nullable=True, default='', comment='项目名称')
    buy_price = Column(DECIMAL(10, 2), nullable=True, comment='采购价')
    sell_price = Column(DECIMAL(10, 2), nullable=True, comment='销售价')
    customer_price = Column(DECIMAL(10, 2), nullable=True, comment='客户价')
    quantity = Column(DECIMAL(10, 2), nullable=True, comment='数量')
    discount = Column(DECIMAL(10, 2), nullable=True, comment='折扣')
    customer_discount = Column(DECIMAL(10, 2), nullable=True, comment='客户折扣')
    total_amount = Column(DECIMAL(10, 2), nullable=True, comment='总金额')
    total_profit = Column(DECIMAL(10, 2), nullable=True, comment='总利润')
    is_customer_discount = Column(Integer, nullable=True, comment='是否允许客户折扣')
    product_uid = Column(String(255), nullable=True, default='', comment='产品唯一 ID')
    product_barcode = Column(String(255), nullable=True, default='', comment='产品条形码')
    is_weighing = Column(Integer, nullable=True, comment='是否称重')

    update_strategy = UpdateStrategy.INCREMENTAL

    def __repr__(self):
        return f"<TicketItems(ticket_uid='{self.ticket_uid}', id='{self.id}', name='{self.name}')>"
