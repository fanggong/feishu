from app.services.trade import TradeService
from .index_calculate import *
from . import const as c
from app.strategy.strategy import Strategy
import logging


logger = logging.getLogger(__name__)


class BollStrategy(Strategy):
    def __init__(self, trade_service: TradeService, inst_id, terms, period):
        super().__init__(trade_service, inst_id, terms, period)

    def index_define(self):
        return [c.BOLL, c.BOLL_UP, c.BOLL_DOWN]

    @staticmethod
    def calculate_indicators(df):
        df = boll_band(df)
        return df

    def order_signal(self):
        for i in range(len(self.terms)):
            tmp = self.candles[str({'channel': f'{self.channel_prefix}{self.terms[i]}', 'instId': self.inst_id})]
            tmp = self.calculate_indicators(tmp)
        return 0