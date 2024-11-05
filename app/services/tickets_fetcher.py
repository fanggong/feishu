from app.services.data_fetcher import DataFetcher
from app.yinbao.Sales import SalesApi
from app.config import Config
from itertools import chain
from app.utils.decorators import retry
import logging

logger = logging.getLogger(__name__)


class TicketsFetcher(DataFetcher):
    @retry(max_retries=5, delay=1)
    def fetch_data(self, start_time, end_time):
        logger.info(f'SERVICE IS RUNNING...')
        sales_api = SalesApi(**Config.get_yinbao_keys())
        tmp = sales_api.get_tickets(start_time=start_time, end_time=end_time)
        if tmp['status'] == 'success':
            dat = tmp['data']['result']
            while len(tmp['data']['result']) == int(tmp['data']['pageSize']):
                tmp = sales_api.get_tickets(
                    start_time=start_time, end_time=end_time, post_back_param=tmp['data']['postBackParameter']
                )
                if tmp['status'] == 'success':
                    dat = dat + tmp['data']['result']
                else:
                    return []
        else:
            return []
        if dat:
            dat = [list(item) for item in list(zip(*[self.process_data(each) for each in dat]))]
            dat[1] = list(chain.from_iterable(dat[1]))
        return dat

    def process_data(self, item):
        ticket_items = item.pop('items', {})
        for each in ticket_items:
            each.update({'ticket_uid': item['uid']})
        payments = item.pop('payments', {})
        payments = payments[0]
        ticket_on_table = item.pop('ticketOnTable', {})
        ticket_spend_detail = item.pop('ticketSpendDetail', {})
        item.update(payments)
        item.update(ticket_on_table)
        item.update(ticket_spend_detail)

        key_mapping = {
            'ticket_uid': 'ticket_uid',
            'id': 'id',
            'name': 'name',
            'buyPrice': 'buy_price',
            'sellPrice': 'sell_price',
            'customerPrice': 'customer_price',
            'quantity': 'quantity',
            'discount': 'discount',
            'customerDiscount': 'customer_discount',
            'totalAmount': 'total_amount',
            'totalProfit': 'total_profit',
            'isCustomerDiscount': 'is_customer_discount',
            'productUid': 'product_uid',
            'productBarcode': 'product_barcode',
            'isWeighing': 'is_weighing'
        }
        ticket_items = [self.process_keys(each, key_mapping) for each in ticket_items]

        key_mapping = {
            # 'ticketDeliveryTypeId': 'ticket_delivery_type_id',
            'cashierUid': 'cashier_uid',
            'customerUid': 'customer_uid',
            'uid': 'uid',
            'sn': 'sn',
            'datetime': 'datetime',
            'totalAmount': 'total_amount',
            'totalProfit': 'total_profit',
            'discount': 'discount',
            'rounding': 'rounding',
            'ticketType': 'ticket_type',
            'invalid': 'invalid',
            'sysUpdateTime': 'sys_update_time',
            'remark': 'remark',
            'serviceFee': 'service_fee',
            'couponFee': 'coupon_fee',
            # 'jobNumber': 'job_number',
            # 'name': 'name',
            'code': 'code',
            'amount': 'amount',
            # 'tableNumber': 'table_number',
            # 'tableName': 'table_name',
            # 'tableUid': 'table_uid',
            # 'tableAreaUid': 'table_area_uid',
            # 'tableCardNo': 'table_card_no',
            # 'peopleNum': 'people_num',
            # 'spendOutStore': 'spend_out_store'
        }
        item = self.process_keys(item, key_mapping)

        return [item, ticket_items]