from app.services.data_fetcher import DataFetcher
from app.okx.Funding import FundingAPI
from app.config import Config
import time
from app.utils.decorators import retry
import logging

logger = logging.getLogger(__name__)


class DepositHistoryFetcher(DataFetcher):
    @retry(max_retries=5, delay=1)
    def fetch_data(self, **kwargs):
        logger.info(f'SERVICE IS RUNNING...')
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
            'from': 'from',
            'fromWdId': 'from_wd_id',
            'state': 'state',
            'to': 'to',
            'ts': 'ts',
            'txId': 'tx_id'
        }
        item['ts'] = self.from_timestamp(item['ts'])
        processed_item = self.process_keys(item, key_mapping)
        return processed_item

    def _get_deposit_history(self, **kwargs):
        funding_api = FundingAPI(**Config.get_okx_keys(), flag='0')
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