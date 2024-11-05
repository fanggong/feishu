from app.services.data_fetcher import DataFetcher
from app.yinbao.Customers import CustomersApi
from app.config import Config
from app.utils.decorators import retry
import logging

logger = logging.getLogger(__name__)


class CustomersFetcher(DataFetcher):
    @retry(max_retries=5, delay=1)
    def fetch_data(self, **kwargs):
        logger.info(f'SERVICE IS RUNNING...')
        dat = CustomersApi(**Config.get_yinbao_keys()).get_customers()
        if dat['status'] == 'success':
            dat = dat['data']['result']
            dat = [self.process_data(item) for item in dat]
            return dat
        else:
            return []

    def process_data(self, item):
        key_mapping = {
            'customerUid': 'customer_uid',
            'categoryName': 'category_name',
            'number': 'number',
            'name': 'name',
            'point': 'point',
            'discount': 'discount',
            'balance': 'balance',
            'phone': 'phone',
            'birthday': 'birthday',
            'qq': 'qq',
            'email': 'email',
            'address': 'address',
            'createdDate': 'create_at',
            'updateDateTime': 'update_at',
            'onAccount': 'on_account',
            'enable': 'enable',
            'sex': 'sex',
            'totalPoint': 'total_point',
            'totalTicketAmount': 'total_ticket_amount',
            'totalRechargeAmount': 'total_recharge_amount',
            'totalTicketNum': 'total_ticket_num',
            'amountInArrear': 'amount_in_arrear'
        }
        ext_info = item.pop('extInfo', {})
        item.update(ext_info)
        item = self.process_keys(item, key_mapping)
        return item