from sqlalchemy import Column, String, DECIMAL
from app.database.mysql import Base


class BalanceOnChain(Base):
    __scope__ = 'crypto'
    __tablename__ = 'balance_on_chain'

    mint = Column(String(255), nullable=False, default='', comment='合约地址')
    amount = Column(DECIMAL(38, 18), nullable=True, comment='数量')
    name = Column(String(255), nullable=False, default='', comment='币种名称')
    symbol = Column(String(255), nullable=False, default='', comment='币种symbol')
    chain = Column(String(255), nullable=False, default='', comment='链名，sol，evm等')
    network = Column(String(255), nullable=False, default='', comment='网络，mainnet，eth等')
    address = Column(String(255), nullable=False, default='', comment='钱包地址')

    def __repr__(self):
        return (f"<BalanceOnChain(mint='{self.mint}', amount={self.amount}, name='{self.name}', "
                f"symbol='{self.symbol}', chain='{self.chain}', network='{self.network}', "
                f"address='{self.address}')>")
