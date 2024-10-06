from database.Mysql import MysqlEngine
from funcs.utils import *
from funcs.const import CUSTOMERS
from yinbao.Customers import CustomersApi


def synchronous_customers(conn: MysqlEngine, customers_api: CustomersApi):
    columns = {
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
    dat = customers_api.get_customers()['data']['result']
    for item in dat:
        ext_info = item.pop('extInfo', {})
        item.update(ext_info)
    dat = pd.DataFrame(dat)
    dat = dat[columns.keys()]
    dat = dat.replace({'': None})
    dat = dat.rename(columns=columns)
    conn.replace_dat(dat=dat, tbl_name=CUSTOMERS)
