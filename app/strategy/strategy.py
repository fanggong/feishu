from abc import ABC, abstractmethod

from app.services.candles_fetcher import CandlesFetcher
from app.okx.websocket.WsPublicAsync import WsPublicAsync
from app.services.trade import TradeService

import asyncio
import json
import time
import logging
from app.config import Config
from threading import Thread, Lock
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from .utils import *


logger = logging.getLogger(__name__)


class Strategy(ABC):
    def __init__(self, trade_service: TradeService, inst_id, terms, period):
        self.trade_service = trade_service
        self.inst_id = inst_id
        self.terms = terms
        self.period = period
        self.channel_prefix = 'mark-price-candle'
        self.indexes = self.index_define()

        self.latest_candle = {'complete': {}, 'incomplete': {}}
        self.ws_latest_candle = None
        self.candles = {}

        httpx_logger = logging.getLogger('httpx')
        httpx_logger.setLevel(logging.WARNING)

        ws_public_logger = logging.getLogger('WsPublic')
        ws_public_logger.setLevel(logging.WARNING)

        werkzeug_logger = logging.getLogger('werkzeug')
        werkzeug_logger.setLevel(logging.WARNING)

    @abstractmethod
    def index_define(self):
        pass

    @staticmethod
    @abstractmethod
    def calculate_indicators(df):
        pass

    @abstractmethod
    def order_signal(self):
        pass

    def strategy_init(self):
        """
        策略初始化，获取历史K线数据
        """
        candle_fetcher = CandlesFetcher()
        for term in self.terms:
            term_key = {'channel': f'{self.channel_prefix}{term}', 'instId': self.inst_id}
            self.candles[str(term_key)] = candle_fetcher.fetch_data(instId=self.inst_id, bar=term)
            self.candles[str(term_key)] = self.calculate_indicators(self.candles[str(term_key)])


    async def handle_websocket(self, args):
        """
        订阅推送
        """
        def message_handle(message):
            """
            处理websocket推送
            """
            message = json.loads(message)
            if 'event' in message.keys():
                return

            arg = message['arg']
            data = message['data'][0]
            status_key = 'incomplete' if data[-1] == '0' else 'complete'
            self.latest_candle[status_key][str(arg)] = data
            self.ws_latest_candle = data

        ws_public = WsPublicAsync(Config.get_ws_public_url())
        await ws_public.start()
        await ws_public.subscribe([args], message_handle)
        while True:
            await asyncio.sleep(60)

    async def ws_main(self):
        """
        订阅所有推送
        """
        tasks = []
        for term in self.terms:
            tasks.append(self.handle_websocket({'channel': f'{self.channel_prefix}{term}', 'instId': self.inst_id}))
        await asyncio.gather(*tasks)

    def ws_thread(self):
        """
        处理推送thread
        """
        asyncio.run(self.ws_main())

    def cal_thread(self):
        """
        处理各种指标计算、多空信号判断
        """
        while True:
            time.sleep(self.period)
            start = time.perf_counter()
            for arg, dat in self.latest_candle['incomplete'].items():
                # 如果存在完整K线，先更新完整K线再插入新的不完整K线
                if self.latest_candle['complete'].get(arg):
                    complete_candle = self.latest_candle['complete'].pop(arg)
                    self.candles[arg] = update_last_row(self.candles[arg], complete_candle)
                    self.candles[arg] = insert_last_row(self.candles[arg], dat)
                # 如果不存在完整K线，直接更新不完整K线
                else:
                    self.candles[arg] = update_last_row(self.candles[arg], dat)
            signal = self.order_signal()
            signal_dict = {1: 'long', 0: 'inoperation', -1: 'short'}
            signal = signal_dict[signal]
            end = time.perf_counter()
            logger.info(f'handle:{signal.ljust(12)}  value:{self.ws_latest_candle[4].ljust(12)}  run time:{end - start} s')

    def kline_thread(self):
        """
        K线可视化
        """
        app = Dash(__name__)

        figure = generate_kline_figure(self.candles, indexes=self.indexes)

        app.layout = html.Div([
            dcc.Graph(
                id='kline-graph',
                figure=figure
            ),
            dcc.Interval(
                id='interval-update',
                interval=self.period * 1000,  # 每10秒触发一次（单位：毫秒）
                n_intervals=0
            )
        ])

        # 定义回调来更新图表
        @app.callback(
            Output('kline-graph', 'figure'),
            Input('interval-update', 'n_intervals')
        )
        def update_figure(n):
            return generate_kline_figure(self.candles, indexes=self.indexes)

        app.run_server(debug=False, use_reloader=False, threaded=True)

        # 自动打开浏览器
        # webbrowser.open("http://127.0.0.1:8050")

    def run(self):
        """
        主函数
        """
        while True:
            try:
                self.strategy_init()
                thread_ws = Thread(target=self.ws_thread)
                thread_ws.start()

                thread_cal = Thread(target=self.cal_thread)
                thread_cal.start()

                thread_kline = Thread(target=self.kline_thread)
                thread_kline.start()

                thread_ws.join()
                thread_cal.join()
                thread_kline.join()
                break
            except Exception as e:
                logger.info(f'发生错误，正在重新启动连接：{e}')
                time.sleep(5)



