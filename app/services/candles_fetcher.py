from app.services.data_fetcher import DataFetcher
from app.okx.MarketData import MarketAPI
from app.config import Config
import numpy as np
import pandas as pd
import logging

logger = logging.getLogger(__name__)


class CandlesFetcher(DataFetcher):
    def fetch_data(self, instId, **kwargs):
        logger.info(f'{kwargs} SERVICE IS RUNNING...')
        market_api = MarketAPI(**Config.get_okx_keys(), debug=False)
        dat = market_api.get_mark_price_candlesticks(instId=instId, **kwargs)
        if dat['code'] == '0':
            dat = dat['data']
            dat = self.process_data(dat)
            logger.info(f'{kwargs} {len(dat)} items getodaze !!!')
            return dat
        else:
            logger.info(f'{kwargs} no data available !!!')
            return []

    @staticmethod
    def process_data(dat: list):
        df = pd.DataFrame(
            reversed(dat),
            columns=['ts', 'open', 'high', 'low', 'close', 'confirm'],
            dtype=float
        )
        return df
