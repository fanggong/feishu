from include.services.data_fetcher import DataFetcher
from include.okx.Funding import FundingAPI
import time
import logging

logger = logging.getLogger(__name__)


class WithdrawHistoryFetcher(DataFetcher):
    def __init__(self, api_key, api_secret_key, passphrase, proxy=None):
        self.api_key = api_key
        self.api_secret_key = api_secret_key
        self.passphrase = passphrase
        self.proxy = proxy

    def fetch_data(self, **kwargs):
        logger.info(f'获取数据 Withdraw History')
        dat = self._get_withdraw_history(**kwargs)
        dat = [self.process_data(item) for item in dat]
        return dat

    def process_data(self, item):
        key_mapping = {
            'chain': 'chain',
            'areaCodeFrom': 'area_code_from',
            'clientId': 'client_id',
            'fee': 'fee',
            'amt': 'amt',
            'txId': 'tx_id',
            'areaCodeTo': 'area_code_to',
            'ccy': 'ccy',
            'from': 'from_s',
            'to': 'to_s',
            'state': 'state',
            'nonTradableAsset': 'non_tradable_asset',
            'ts': 'ts',
            'wdId': 'wd_id',
            'feeCcy': 'fee_ccy'
        }
        item['ts'] = self.from_timestamp(item['ts'])
        processed_item = self.process_keys(item, key_mapping)
        return processed_item

    def _get_withdraw_history(self, **kwargs):
        funding_api = FundingAPI(
            api_key=self.api_key, api_secret_key=self.api_secret_key,
            passphrase=self.passphrase, proxy=self.proxy, flag='0'
        )
        dat = funding_api.get_withdrawal_history(**kwargs)
        if dat['code'] == '0':
            dat = dat.get('data')
            time.sleep(0.2)
            if len(dat) == 0:
                return dat
            else:
                kwargs['after'] = dat[-1]['ts']
                dat = dat + self._get_withdraw_history(**kwargs)
                return dat
        else:
            return []