import logging
import time

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
    strategy = BollStrategy(
        ws_public_url='wss://ws.okx.com:8443/ws/v5/business', trade_service=trade_service,
        channel='candle5m', instId='WLD-USDT-SWAP'
    )
    strategy.run(bar='5m')
