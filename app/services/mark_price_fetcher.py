from app.services.data_fetcher import DataFetcher
from app.okx.PublicData import PublicAPI
from app.config import Config
from app.utils.decorators import retry
import logging

logger = logging.getLogger(__name__)


class MarkPriceFetcher(DataFetcher):
    @retry(max_retries=5, delay=1)
    def fetch_data(self, instType, **kwargs):
        logger.info(f'SERVICE IS RUNNING...')
        dat = PublicAPI(**Config.get_okx_keys(), flag='0').get_mark_price(instType, **kwargs)
        if dat['code'] == '0':
            dat = dat['data']
            dat = [self.process_data(item) for item in dat]
            return dat
        else:
            return []

    def process_data(self, item):
        key_mapping = {
            'instType': 'inst_type',
            'instId': 'inst_id',
            'markPx': 'mark_px',
            'ts': 'ts'
        }
        item['ts'] = self.from_timestamp(item['ts'])
        item = self.process_keys(item, key_mapping)
        return item