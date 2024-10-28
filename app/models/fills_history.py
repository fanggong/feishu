from sqlalchemy import Column, String, DECIMAL, DateTime, Integer
from app.database.mysql import Base


class FillsHistory(Base):
    __scope__ = 'crypto'
    __tablename__ = 'fills_history'

    inst_type = Column(String(255), nullable=True, default='', comment='产品类型')
    inst_id = Column(String(255), nullable=True, default='', comment='产品 ID')
    trade_id = Column(String(255), nullable=True, default='', comment='最新成交 ID')
    ord_id = Column(String(255), nullable=True, default='', comment='订单 ID')
    cl_ord_id = Column(String(255), nullable=True, default='', comment='用户自定义订单ID')
    bill_id = Column(String(255), primary_key=True, nullable=False, default='', comment='账单ID')
    tag = Column(String(255), nullable=True, default='', comment='订单标签')
    fill_px = Column(DECIMAL(38, 16), nullable=True, comment='最新成交价格，同"账单流水查询"的 px')
    fill_sz = Column(DECIMAL(38, 16), nullable=True, comment='最新成交数量')
    side = Column(String(255), nullable=True, default='', comment='订单方向 buy：买 sell：卖')
    pos_side = Column(String(255), nullable=True, default='', comment='持仓方向 long：多 short：空 买卖模式返回 net')
    exec_type = Column(String(255), nullable=True, default='', comment='流动性方向 T：taker M：maker 不适用于系统订单比如强平和ADL')
    fee_ccy = Column(String(255), nullable=True, default='', comment='交易手续费币种或者返佣金币种')
    fee = Column(DECIMAL(38, 16), nullable=True, comment='手续费金额或者返佣金额 手续费扣除为‘负数’，如 -0.01 手续费返佣为‘正数’，如 0.01')
    ts = Column(DateTime, nullable=True, comment='成交明细产生时间，Unix时间戳的毫秒数格式，如 1597026383085')
    sub_type = Column(Integer, nullable=True, comment='成交类型')

    def __repr__(self):
        return f"<FillsHistory(bill_id='{self.bill_id}', inst_id='{self.inst_id}', trade_id='{self.trade_id}')>"
