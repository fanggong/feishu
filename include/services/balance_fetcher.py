from include.services.data_fetcher import DataFetcher
from include.okx.Account import AccountAPI
import logging

logger = logging.getLogger(__name__)


class BalanceFetcher(DataFetcher):
    def __init__(self, api_key, api_secret_key, passphrase, proxy=None):
        self.api_key = api_key
        self.api_secret_key = api_secret_key
        self.passphrase = passphrase
        self.proxy = proxy

    def fetch_data(self):
        logger.info(f'获取数据 Balance')
        dat = AccountAPI(
            api_key=self.api_key, api_secret_key=self.api_secret_key,
            passphrase=self.passphrase, proxy=self.proxy, flag='0'
        ).get_account_balance()
        if dat['code'] == '0':
            dat = dat['data'][0]['details']
            dat = [self.process_data(item) for item in dat]
            return dat
        else:
            return []

    def process_data(self, item):
        key_mapping = {
            'accAvgPx': 'acc_avg_px',
            'availBal': 'avail_bal',
            'availEq': 'avail_eq',
            'borrowFroz': 'borrow_froz',
            'cashBal': 'cash_bal',
            'ccy': 'ccy',
            'clSpotInUseAmt': 'cl_spot_in_use_amt',
            'crossLiab': 'cross_liab',
            'disEq': 'dis_eq',
            'eq': 'eq',
            'eqUsd': 'eq_usd',
            'fixedBal': 'fixed_bal',
            'frozenBal': 'frozen_bal',
            'imr': 'imr',
            'interest': 'interest',
            'isoEq': 'iso_eq',
            'isoLiab': 'iso_liab',
            'isoUpl': 'iso_upl',
            'liab': 'liab',
            'maxLoan': 'max_loan',
            'maxSpotInUse': 'max_spot_in_use',
            'mgnRatio': 'mgn_ratio',
            'mmr': 'mmr',
            'notionalLever': 'notional_lever',
            'openAvgPx': 'open_avg_px',
            'ordFrozen': 'ord_frozen',
            'rewardBal': 'reward_bal',
            'smtSyncEq': 'smt_sync_eq',
            'spotBal': 'spot_bal',
            'spotInUseAmt': 'spot_in_use_amt',
            'spotIsoBal': 'spot_iso_bal',
            'spotUpl': 'spot_upl',
            'spotUplRatio': 'spot_upl_ratio',
            'stgyEq': 'stgy_eq',
            'totalPnl': 'total_pnl',
            'totalPnlRatio': 'total_pnl_ratio',
            'twap': 'twap',
            'uTime': 'u_time',
            'upl': 'upl',
            'uplLiab': 'upl_liab'
        }
        item['uTime'] = self.from_timestamp(item['uTime'])
        processed_item = self.process_keys(item, key_mapping)
        return processed_item