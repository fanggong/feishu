from app.services.data_fetcher import DataFetcher
from okx.Account import AccountAPI
from app.config import Config
import time


class BillsHistoryFetcher(DataFetcher):
    def fetch_data(self, **kwargs):
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
        account_api = AccountAPI(**Config.get_okx_keys(), flag='0')
        dat = account_api.get_account_bills_archive(**kwargs)
        if dat['code'] == '0':
            dat = dat.get('data')
            time.sleep(0.4)
            if len(dat) == 0:
                return dat
            else:
                kwargs['before'] = dat[0]['billId']
                dat = dat + self._get_bills_history(**kwargs)
                return dat
        else:
            return []