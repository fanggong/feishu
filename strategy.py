import logging
import time
from distutils.command.install_data import install_data

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s][%(asctime)s][%(name)s] %(message)s',
    handlers=[
        logging.FileHandler("output.log"),  # 将日志输出到 output.log 文件
        logging.StreamHandler()  # 同时输出到控制台
    ]
)
from app.strategy.boll import BollStrategy
from app.services.trade import TradeService
import pandas as pd

pd.set_option('display.max_columns', None)


if __name__ == '__main__':
    trade_service = TradeService(key_type='main')
    strategy = BollStrategy(trade_service=trade_service, inst_id='BTC-USDT-SWAP', short_term='5m', long_term='1H')
    strategy.run()
