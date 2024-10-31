from app.services.data_fetcher import DataFetcher
from app.okx.Account import AccountAPI
from app.config import Config
from app.utils.decorators import retry


class PositionsFetcher(DataFetcher):
    @retry(max_retries=3, delay=2, exceptions=(TimeoutError, ConnectionError))
    def fetch_data(self, **kwargs):
        dat = AccountAPI(**Config.get_okx_keys(), flag='0').get_positions(**kwargs)
        if dat['code'] == '0':
            dat = dat['data']
            dat = [self.process_data(item) for item in dat]
            return dat
        else:
            return []

    def process_data(self, item):
        key_mapping = {
            'adl': 'adl',
            'availPos': 'avail_pos',
            'avgPx': 'avg_px',
            'baseBal': 'base_bal',
            'baseBorrowed': 'base_borrowed',
            'baseInterest': 'base_interest',
            'bePx': 'be_px',
            'bizRefId': 'biz_ref_id',
            'bizRefType': 'biz_ref_type',
            'cTime': 'c_time',
            'ccy': 'ccy',
            'clSpotInUseAmt': 'cl_spot_in_use_amt',
            'closeOrderAlgo': 'close_order_algo',
            'deltaBS': 'delta_bs',
            'deltaPA': 'delta_pa',
            'fee': 'fee',
            'fundingFee': 'funding_fee',
            'gammaBS': 'gamma_bs',
            'gammaPA': 'gamma_pa',
            'idxPx': 'idx_px',
            'imr': 'imr',
            'instId': 'inst_id',
            'instType': 'inst_type',
            'interest': 'interest',
            'last': 'last',
            'lever': 'lever',
            'liab': 'liab',
            'liabCcy': 'liab_ccy',
            'liqPenalty': 'liq_penalty',
            'liqPx': 'liq_px',
            'margin': 'margin',
            'markPx': 'mark_px',
            'maxSpotInUseAmt': 'max_spot_in_use_amt',
            'mgnMode': 'mgn_mode',
            'mgnRatio': 'mgn_ratio',
            'mmr': 'mmr',
            'notionalUsd': 'notional_usd',
            'optVal': 'opt_val',
            'pendingCloseOrdLiabVal': 'pending_close_ord_liab_val',
            'pnl': 'pnl',
            'pos': 'pos',
            'posCcy': 'pos_ccy',
            'posId': 'pos_id',
            'posSide': 'pos_side',
            'quoteBal': 'quote_bal',
            'quoteBorrowed': 'quote_borrowed',
            'quoteInterest': 'quote_interest',
            'realizedPnl': 'realized_pnl',
            'spotInUseAmt': 'spot_in_use_amt',
            'spotInUseCcy': 'spot_in_use_ccy',
            'thetaBS': 'theta_bs',
            'thetaPA': 'theta_pa',
            'tradeId': 'trade_id',
            'uTime': 'u_time',
            'upl': 'upl',
            'uplLastPx': 'upl_last_px',
            'uplRatio': 'upl_ratio',
            'uplRatioLastPx': 'upl_ratio_last_px',
            'usdPx': 'usd_px',
            'vegaBS': 'vega_bs',
            'vegaPA': 'vega_pa'
        }
        item['closeOrderAlgo'] = None
        item['uTime'] = self.from_timestamp(item['uTime'])
        item['cTime'] = self.from_timestamp(item['cTime'])
        item = self.process_keys(item, key_mapping)
        return item
