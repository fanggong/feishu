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

    @staticmethod
    def find_inflection_point(l):
        l = l.tolist()
        # max_index = l.index(max(l))
        min_index = l.index(min(l))
        return min_index

    def signal_dict(self):
        return {
            0: 'inoperation'
        }

    def order_signal(self):
        for i in range(len(self.terms)):
            candle: pd.DataFrame = self.candles[str({'channel': f'{self.channel_prefix}{self.terms[i]}', 'instId': self.inst_id})]
            candle = self.calculate_indicators(candle)
            candle = candle.dropna()
            # inflection_index = self.find_inflection_point(candle[c.BOLL])
            #
            # before = candle[c.BOLL].iloc[0:(inflection_index+1)]
            # after = candle[c.BOLL].iloc[inflection_index:]
            #
            # if before < 15 or after < 15:
            #     pass

        return 0