from include.services.data_fetcher import DataFetcher
from include.okx.Funding import FundingAPI
import time
import logging

logger = logging.getLogger(__name__)


class DepositHistoryFetcher(DataFetcher):
    def __init__(self, api_key, api_secret_key, passphrase, proxy=None):
        self.api_key = api_key
        self.api_secret_key = api_secret_key
        self.passphrase = passphrase
        self.proxy = proxy

    def fetch_data(self, **kwargs):
        logger.info(f'获取数据 Deposit History')
        dat = self._get_deposit_history(**kwargs)
        dat = [self.process_data(item) for item in dat]
        return dat

    def process_data(self, item):
        key_mapping = {
            'actualDepBlkConfirm': 'actual_dep_blk_confirm',
            'amt': 'amt',
            'areaCodeFrom': 'area_code_from',
            'ccy': 'ccy',
            'chain': 'chain',
            'depId': 'dep_id',
            'from': 'from_s',
            'fromWdId': 'from_wd_id',
            'state': 'state',
            'to': 'to_s',
            'ts': 'ts',
            'txId': 'tx_id'
        }
        item['ts'] = self.from_timestamp(item['ts'])
        processed_item = self.process_keys(item, key_mapping)
        return processed_item

    def _get_deposit_history(self, **kwargs):
        funding_api = FundingAPI(
            api_key=self.api_key, api_secret_key=self.api_secret_key,
            passphrase=self.passphrase, proxy=self.proxy, flag='0'
        )
        dat = funding_api.get_deposit_history(**kwargs)
        if dat['code'] == '0':
            dat = dat.get('data')
            time.sleep(0.2)
            if len(dat) == 0:
                return dat
            else:
                kwargs['after'] = dat[-1]['ts']
                dat = dat + self._get_deposit_history(**kwargs)
                return dat
        else:
            return []