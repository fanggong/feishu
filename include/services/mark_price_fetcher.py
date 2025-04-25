from include.services.data_fetcher import DataFetcher
from include.okx.PublicData import PublicAPI
import logging

logger = logging.getLogger(__name__)


class MarkPriceFetcher(DataFetcher):
    def __init__(self, api_key, api_secret_key, passphrase, proxy=None):
        self.api_key = api_key
        self.api_secret_key = api_secret_key
        self.passphrase = passphrase
        self.proxy = proxy

    def fetch_data(self, instType, **kwargs):
        logger.info(f'获取数据 Mark Price')
        dat = PublicAPI(
            api_key=self.api_key, api_secret_key=self.api_secret_key,
            passphrase=self.passphrase, proxy=self.proxy, flag='0'
        ).get_mark_price(instType, **kwargs)
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