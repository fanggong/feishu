import pandas as pd

from funcs.const import PRODUCTS
from funcs.utils import *
from yinbao.Products import ProductsApi
from database.Mysql import MysqlEngine


def synchronous_product(conn: MysqlEngine, products_api: ProductsApi):
    columns = {
        'uid': 'uid',
        'categoryUid': 'category_uid',
        'name': 'name',
        'barcode': 'barcode',
        'buyPrice': 'buy_price',
        'sellPrice': 'sell_price',
        'sellPrice2': 'sell_price2',
        'stock': 'stock',
        'maxStock': 'max_stock',
        'minStock': 'min_stock',
        'noStock': 'no_stock',
        'pinyin': 'pinyin',
        'customerPrice': 'customer_price',
        'description': 'description',
        'isCustomerDiscount': 'is_customer_discount',
        'supplierUid': 'supplier_uid',
        'enable': 'enable',
        'productionDate': 'production_at',
        'createdDatetime': 'create_at',
        'updatedDatetime': 'update_at'
    }
    tmp = products_api.get_products()['data']

    dat = tmp['result']
    while len(tmp['result']) == int(tmp['pageSize']):
        tmp = products_api.get_products(post_back_param=tmp['postBackParameter'])['data']
        dat = dat + tmp['result']
    dat = pd.DataFrame(dat)
    dat = dat[columns.keys()]
    dat = dat.replace({'': None})
    dat = dat.rename(columns=columns)
    conn.upsert_dat(dat=dat, tbl_name=PRODUCTS)

