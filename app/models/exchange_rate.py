from sqlalchemy import Column, DECIMAL
from app.database.mysql import Base


class ExchangeRate(Base):
    __scope__ = 'crypto'
    __tablename__ = 'exchange_rate'

    usd_cny = Column(DECIMAL(38, 16), nullable=True, comment='人民币兑美元汇率')

    def __repr__(self):
        return f"<ExchangeRate(usd_cny={self.usd_cny})>"
