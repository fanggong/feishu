from app.services.data_fetcher import DataFetcher
from app.config import Config
from app.yinbao.Products import ProductsApi
from app.utils.decorators import retry


class ProductsFetcher(DataFetcher):
    @retry(max_retries=3, delay=2, exceptions=(TimeoutError, ConnectionError))
    def fetch_data(self, **kwargs):
        products_api = ProductsApi(**Config.get_yinbao_keys())
        tmp = products_api.get_products()
        if tmp['status'] == 'success':
            dat = tmp['data']['result']
            while len(tmp['data']['result']) == int(tmp['data']['pageSize']):
                tmp = products_api.get_products(post_back_param=tmp['data']['postBackParameter'])
                if tmp['status'] == 'success':
                    dat = dat + tmp['data']['result']
                else:
                    return []
        else:
            return []
        dat = [self.process_data(item) for item in dat]
        return dat

    def process_data(self, item):
        key_mapping = {
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
        item = self.process_keys(item, key_mapping)
        return item