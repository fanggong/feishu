from include.services.data_fetcher import DataFetcher
from include.okx.PublicData import PublicAPI
import logging

logger = logging.getLogger(__name__)


class InstrumentsFetcher(DataFetcher):
    def __init__(self, api_key, api_secret_key, passphrase, proxy=None):
        self.api_key = api_key
        self.api_secret_key = api_secret_key
        self.passphrase = passphrase
        self.proxy = proxy

    def fetch_data(self, instType, **kwargs):
        logger.info(f'获取数据 Instruments')
        dat = PublicAPI(
            api_key=self.api_key, api_secret_key=self.api_secret_key,
            passphrase=self.passphrase, proxy=self.proxy, flag='0'
        ).get_instruments(instType, **kwargs)
        if dat['code'] == '0':
            dat = dat['data']
            dat = [self.process_data(item) for item in dat]
            return dat
        else:
            return []

    def process_data(self, item):
        key_mapping = {
            'alias': 'alias',
            'baseCcy': 'base_ccy',
            'category': 'category',
            'ctMult': 'ct_mult',
            'ctType': 'ct_type',
            'ctVal': 'ct_val',
            'ctValCcy': 'ct_val_ccy',
            'expTime': 'exp_time',
            'instFamily': 'inst_family',
            'instId': 'inst_id',
            'instType': 'inst_type',
            'lever': 'level',
            'listTime': 'list_time',
            'lotSz': 'lot_sz',
            'maxIcebergSz': 'max_iceberg_sz',
            'maxLmtAmt': 'max_lmt_amt',
            'maxLmtSz': 'max_lmt_sz',
            'maxMktAmt': 'max_mkt_amt',
            'maxMktSz': 'max_mkt_sz',
            'maxStopSz': 'max_stop_sz',
            'maxTriggerSz': 'max_trigger_sz',
            'maxTwapSz': 'max_twap_sz',
            'minSz': 'min_sz',
            'optType': 'opt_type',
            'quoteCcy': 'quote_ccy',
            'ruleType': 'rule_type',
            'settleCcy': 'settle_ccy',
            'state': 'state',
            'stk': 'stk',
            'tickSz': 'tick_sz',
            'uly': 'uly'
        }
        item['expTime'] = self.from_timestamp(item['expTime'])
        item['listTime'] = self.from_timestamp(item['listTime'])
        item = self.process_keys(item, key_mapping)
        return item