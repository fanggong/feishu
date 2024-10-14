import pandas as pd

from funcs.utils import *
from funcs.const import TICKETS, TICKET_ITEMS
from database.Mysql import MysqlEngine
from yinbao.Sales import SalesApi


def synchronous_tickets(conn: MysqlEngine, sales_api: SalesApi, start_time: str, end_time: str):
    tmp = sales_api.get_tickets(start_time=start_time, end_time=end_time)['data']
    dat = tmp['result']
    while len(tmp['result']) == int(tmp['pageSize']):
        tmp = sales_api.get_tickets(start_time=start_time, end_time=end_time, post_back_param=tmp['postBackParameter'])['data']
        dat = dat + tmp['result']
        # print(f"{len(tmp['result'])}  ----  {int(tmp['pageSize'])}")
    if dat:
        ticket_items = []
        for item in dat:
            # cashier = item.pop('cashier', {})
            items = item.pop('items', {})
            for each in items:
                each.update({'ticket_uid': item['uid']})
            payments = item.pop('payments', {})
            payments = payments[0]
            ticket_on_table = item.pop('ticketOnTable', {})
            ticket_spend_detail = item.pop('ticketSpendDetail', {})
            ticket_items = ticket_items + items
            # item.update(cashier)
            item.update(payments)
            item.update(ticket_on_table)
            item.update(ticket_spend_detail)

        columns = {
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
        ticket_items = pd.DataFrame(ticket_items)
        ticket_items = ticket_items[columns.keys()]
        ticket_items = ticket_items.rename(columns=columns)

        columns = {
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
        dat = pd.DataFrame(dat)
        dat = dat[columns.keys()]
        dat = dat.rename(columns=columns)

        conn.upsert_dat(dat=ticket_items, tbl_name=TICKET_ITEMS)
        conn.upsert_dat(dat=dat, tbl_name=TICKETS)