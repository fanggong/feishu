from app.services.data_fetcher import DataFetcher
from app.okx.MarketData import MarketAPI
from app.config import Config
import numpy as np
import pandas as pd
import logging

logger = logging.getLogger(__name__)


class CandlesFetcher(DataFetcher):
    def fetch_data(self, instId, **kwargs):
        logger.info(f'SERVICE IS RUNNING...')
        market_api = MarketAPI(**Config.get_okx_keys(), debug=False)
        dat = market_api.get_candlesticks(instId=instId, **kwargs)
        if dat['code'] == '0':
            dat = dat['data']
            dat = self.process_data(dat)
            return dat
        else:
            return []

    @staticmethod
    def process_data(dat: list):
        df = pd.DataFrame(
            reversed(dat),
            columns=['ts', 'open', 'high', 'low', 'close', 'vol', 'vol_ccy', 'vol_ccy_quote', 'confirm'],
            dtype=float
        )
        return df
