import logging
import os
from datetime import datetime


log_filename = datetime.now().strftime('strategy_%Y%m%d%H%M%S.log')
log_path = os.path.join('log', log_filename)

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s][%(asctime)s][%(name)s] %(message)s',
    handlers=[logging.FileHandler(log_path), logging.StreamHandler()]
)
from app.strategy.ma_strategy import MaStrategy
from app.strategy.boll_strategy import BollStrategy
from app.services.trade import TradeService
import pandas as pd

pd.set_option('display.max_columns', None)


if __name__ == '__main__':
    trade_service = TradeService(key_type='main')
    # strategy = MaStrategy(trade_service=trade_service, inst_id='ETH-USDT-SWAP', terms=['5m', '15m', '1H'], period=5)
    strategy = BollStrategy(trade_service=trade_service, inst_id='ETH-USDT', terms=['5m', '15m', '1H', '4H', '1D'], period=5)
    strategy.run()
