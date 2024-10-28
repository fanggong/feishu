from sqlalchemy import Column, String, DECIMAL, Integer, DateTime
from app.database.mysql import Base
from app.services.update_strategy import UpdateStrategy


class Products(Base):
    __scope__ = 'bar'
    __tablename__ = 'products'

    uid = Column(String(255), primary_key=True, nullable=False, default='', comment='产品唯一 ID')
    category_uid = Column(String(255), nullable=True, default='', comment='分类唯一 ID')
    name = Column(String(255), nullable=True, default='', comment='产品名称')
    barcode = Column(String(255), nullable=True, default='', comment='条形码')
    buy_price = Column(DECIMAL(10, 2), nullable=True, comment='采购价')
    sell_price = Column(DECIMAL(10, 2), nullable=True, comment='销售价')
    sell_price2 = Column(DECIMAL(10, 2), nullable=True, comment='销售价2')
    stock = Column(DECIMAL(10, 2), nullable=True, comment='库存')
    max_stock = Column(DECIMAL(10, 2), nullable=True, comment='最大库存')
    min_stock = Column(DECIMAL(10, 2), nullable=True, comment='最小库存')
    no_stock = Column(Integer, nullable=True, comment='缺货标记')
    pinyin = Column(String(255), nullable=True, default='', comment='拼音码')
    customer_price = Column(DECIMAL(10, 2), nullable=True, comment='客户价')
    description = Column(String(255), nullable=True, default='', comment='描述')
    is_customer_discount = Column(Integer, nullable=True, comment='是否允许客户折扣')
    supplier_uid = Column(String(255), nullable=True, default='', comment='供应商唯一 ID')
    enable = Column(Integer, nullable=True, comment='是否启用')
    production_at = Column(DateTime, nullable=True, comment='生产日期')
    create_at = Column(DateTime, nullable=True, comment='创建时间')
    update_at = Column(DateTime, nullable=True, comment='更新时间')
    
    update_strategy = UpdateStrategy.FULL

    def __repr__(self):
        return f"<Products(uid='{self.uid}', name='{self.name}')>"
