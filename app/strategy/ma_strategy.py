from app.services.trade import TradeService
from .index_calculate import *
from . import const as c
from app.strategy.strategy import Strategy
import logging


logger = logging.getLogger(__name__)


class MaStrategy(Strategy):
    def __init__(self, trade_service: TradeService, inst_id, terms, period):
        super().__init__(trade_service, inst_id, terms, period)

    def index_define(self):
        return [c.MA5, c.MA20, c.MA50]

    @staticmethod
    def calculate_indicators(df):
        df = ma5(df)
        df = ma20(df)
        df = ma50(df)
        return df

    def order_signal(self):
        short_df = self.candles[str({'channel': f'{self.channel_prefix}{self.terms[0]}', 'instId': self.inst_id})]
        mid_df = self.candles[str({'channel': f'{self.channel_prefix}{self.terms[1]}', 'instId': self.inst_id})]
        long_df = self.candles[str({'channel': f'{self.channel_prefix}{self.terms[2]}', 'instId': self.inst_id})]

        # 计算短期、中期和长期的技术指标
        short_df = self.calculate_indicators(short_df)
        mid_df = self.calculate_indicators(mid_df)
        long_df = self.calculate_indicators(long_df)

        # 获取短期、中期、长期的最新数据（即最后一行）
        short_last = short_df.iloc[-1]
        mid_last = mid_df.iloc[-1]
        long_last = long_df.iloc[-1]

        # 短期均线金叉或死叉
        short_signal = 0
        if short_last['ma5'] > short_last['ma20']:
            short_signal = 1  # 金叉
        elif short_last['ma5'] < short_last['ma20']:
            short_signal = -1  # 死叉

        # 中期均线金叉或死叉
        mid_signal = 0
        if mid_last['ma20'] > mid_last['ma50']:
            mid_signal = 1  # 金叉
        elif mid_last['ma20'] < mid_last['ma50']:
            mid_signal = -1  # 死叉

        # 长期趋势判断（仅使用50日均线）
        long_signal = 0
        if long_last['ma50'] > long_df['ma50'].iloc[-2]:
            long_signal = 1  # 上升趋势
        elif long_last['ma50'] < long_df['ma50'].iloc[-2]:
            long_signal = -1  # 下降趋势

        # 综合判断：根据短期、中期和长期的趋势进行操作决策
        if short_signal == 1 and mid_signal == 1 and long_signal == 1:
            return 1  # 看多
        elif short_signal == -1 and mid_signal == -1 and long_signal == -1:
            return -1  # 看空
        else:
            return 0  # 不操作


