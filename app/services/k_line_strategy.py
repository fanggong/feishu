import time
from abc import ABC, abstractmethod
from app.okx.websocket.WsPublicAsync import WsPublicAsync
from app.okx.websocket import WsPrivateAsync
from app.services.trade import TradeService
import pandas as pd
import asyncio
import json
import logging

logger = logging.getLogger(__name__)


class KLineStrategy(ABC):
    def __init__(self, ws_public_url: str = None, ws_private_url: str = None,
                 trade_service: TradeService = None, channel='', instId=''):
        self.ws_public_url = ws_public_url
        self.ws_private_url = ws_private_url
        self.trade_service = trade_service
        self.latest_candle = []
        self.channel = channel
        self.instId = instId
        self.candles = None
        # 记录当前K线是否已经下单，理论上同一根K线不多次下单
        self.ordered = 0

    @abstractmethod
    def strategy_init(self):
        # 该方法需要完成对candles的赋值
        # 对应字段需要为ts,open,high,low,close,vol,vol_ccy,vol_ccy_quote,confirm
        self.candles = pd.DataFrame()

    @abstractmethod
    def add_index(self):
        pass

    @abstractmethod
    async def periodic_handle(self):
        # 需要先调用 update_candles() 和 add_index()
        while True:
            await asyncio.sleep(5)
            if self.latest_candle:
                self.update_candles(new_candle=self.latest_candle)
                self.add_index()
                pass

    def message_handle(self, message):
        message = json.loads(message).get('data')
        if message:
            # 推送收到完整K线
            if message[0][-1] == '1':
                self.update_candles(message[0])
                self.add_index()
                self.ordered = 0
                logger.info('当前K线已完整，更新K线')
            # 推送收到不完整K线
            else:
                self.latest_candle = message[0]

    def update_candles(self, new_candle: list):
        self.candles = self.candles.iloc[:-1]
        self.candles = self.candles[['ts', 'open', 'high', 'low', 'close', 'vol', 'vol_ccy', 'vol_ccy_quote', 'confirm']]
        if str(new_candle[-1]) == '1':
            append = pd.DataFrame([[i for i in range(len(new_candle))]], columns=self.candles.columns)
        else:
            append = pd.DataFrame()
        new_candle = pd.DataFrame([[float(item) for item in new_candle]], columns=self.candles.columns)
        self.candles = pd.concat([self.candles, new_candle, append], ignore_index=True)

    async def main(self):
        ws_public = WsPublicAsync(self.ws_public_url)
        await ws_public.start()
        await ws_public.subscribe([{'channel': self.channel, 'instId': self.instId}], self.message_handle)
        asyncio.create_task(self.periodic_handle())
        try:
            while True:
                await asyncio.sleep(1200)
        except asyncio.CancelledError:
            logger.info('WebSocket 连接被取消，正在断开连接...')
            await ws_public.stop()

    def run(self):
        while True:
            try:
                asyncio.run(self.main())
            except Exception as e:
                logger.info(e)
                time.sleep(5)