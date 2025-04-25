from include.services.data_fetcher import DataFetcher
from include.okx.Account import AccountAPI
import time
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class BillsHistoryFetcher(DataFetcher):
    def __init__(self, api_key, api_secret_key, passphrase, proxy=None):
        self.api_key = api_key
        self.api_secret_key = api_secret_key
        self.passphrase = passphrase
        self.proxy = proxy

    def fetch_data(self, **kwargs):
        logger.info(f'获取数据 Bills History')
        dat = self._get_bills_history(**kwargs)
        dat = [self.process_data(item) for item in dat]
        return dat

    def process_data(self, item):
        key_mapping = { 
            'instType': 'inst_type',
            'billId': 'bill_id',
            'subType': 'sub_type',
            'ts': 'ts',
            'balChg': 'bal_chg',
            'posBalChg': 'pos_bal_chg',
            'bal': 'bal',
            'posBal': 'pos_bal',
            'sz': 'sz',
            'px': 'px',
            'ccy': 'ccy',
            'pnl': 'pnl',
            'fee': 'fee',
            'mgnMode': 'mgn_mode',
            'instId': 'inst_id',
            'ordId': 'ord_id',
            'execType': 'exec_type',
            'interest': 'interest',
            'tag': 'tag',
            'fillTime': 'fill_time',
            'tradeId': 'trade_id',
            'clOrdId': 'cl_ord_id',
            'fillIdxPx': 'fill_idx_px',
            'fillMarkPx': 'fill_mark_px',
            'fillPxVol': 'fill_px_vol',
            'fillPxUsd': 'fill_px_usd',
            'fillMarkVol': 'fill_mark_vol',
            'fillFwdPx': 'fill_fwd_px'
        }
        item['ts'] = self.from_timestamp(item['ts'])
        item['fillTime'] = self.from_timestamp(item['fillTime'])
        processed_item = self.process_keys(item, key_mapping)
        return processed_item

    def _get_bills_history(self, **kwargs):
        account_api = AccountAPI(
            api_key=self.api_key, api_secret_key=self.api_secret_key,
            passphrase=self.passphrase, proxy=self.proxy, flag='0'
        )
        dat = account_api.get_account_bills_archive(**kwargs)
        if dat['code'] == '0':
            dat = dat.get('data')
            time.sleep(0.4)
            if len(dat) == 0:
                return dat
            else:
                logger.info(f"{len(dat)} Data from {datetime.fromtimestamp(int(dat[-1]['ts'])/1000)} to {datetime.fromtimestamp(int(dat[0]['ts'])/1000)}")
                kwargs['after'] = dat[-1]['billId']
                dat = dat + self._get_bills_history(**kwargs)
                return dat
        else:
            return []