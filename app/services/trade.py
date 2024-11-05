import uuid

from app.okx.Trade import TradeAPI
from app.okx.Account import AccountAPI
from app.config import Config
from app.utils.decorators import retry
import pandas as pd
import logging

logger = logging.getLogger(__name__)


class TradeService:
    def __init__(self, key_type):
        self.config = Config.get_okx_keys(key_type)
        self.flag = '1' if key_type == 'simulate' else '0'

    @retry(max_retries=10, delay=3)
    def set_leverage(self, instId, lever, mgnMode, posSide):
        account_api = AccountAPI(**self.config, flag=self.flag, debug=False)
        res = account_api.set_leverage(instId=instId, lever=lever, mgnMode=mgnMode, posSide=posSide)
        if res['code'] == '0':
            logger.info(f"Set Leverage {lever} for {instId} on {mgnMode} {posSide}")

    # @retry(max_retries=10, delay=3)
    def get_order_list(self, **kwargs):
        trade_api = TradeAPI(**self.config, flag=self.flag, debug=False)
        dat = trade_api.get_order_list(**kwargs)
        res = pd.DataFrame()
        if dat['code'] == '0' and len(dat['data']) > 0:
            res = pd.DataFrame(dat['data'])
            res = res[['instId', 'clOrdId', 'side', 'posSide', 'sz', 'lever', 'px']]
        return res

    @retry(max_retries=10, delay=3)
    def market_order(self, instId, sz, side, posSide):
        trade_api = TradeAPI(**self.config, flag=self.flag, debug=False)
        res = trade_api.place_order(
            instId=instId, tdMode='isolated', side=side, posSide=posSide, sz=sz, ordType='market'
        )
        if res['code'] == '0':
            logger.info(f'Place Market Order Success: instId: {instId}, sz: {sz}, side: {side} {posSide}')
            return True
        else:
            logger.info(f'Place Market Order Fail: instId: {instId}, sz: {sz}, side: {side} {posSide}')
            return False

    @retry(max_retries=10, delay=3)
    def limit_order(self, instId, sz, px, side, posSide):
        trade_api = TradeAPI(**self.config, flag=self.flag, debug=False)
        cl_ord_id = uuid.uuid4().hex[:16]
        res = trade_api.place_order(
            instId=instId, tdMode='isolated', side=side, posSide=posSide, sz=sz, ordType='limit', px=px,
            clOrdId=cl_ord_id
        )
        if res['code'] == '0':
            logger.info(f'Place Limit Order Success: instId: {instId}, sz: {sz}, px: {px}, side: {side} {posSide}')
            return True
        else:
            logger.info(f'Place Limit Order Fail: instId: {instId}, sz: {sz}, px: {px}, side: {side} {posSide}')
            return False

    @retry(max_retries=10, delay=3)
    def amend_order(self, instId, clOrdId, newPx):
        trade_api = TradeAPI(**self.config, flag=self.flag, debug=False)
        res = trade_api.amend_order(instId=instId, clOrdId=clOrdId, newPx=newPx)
        if res['code'] == '0':
            logger.info(f'Amend Order Success: instId: {instId}, clOrdId: {clOrdId}, newPx: {newPx}')
            return True
        else:
            logger.info(f'Amend Order Fail: instId: {instId}, clOrdId: {clOrdId}, newPx: {newPx}')
            return False