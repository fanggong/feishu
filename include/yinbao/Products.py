from .yinbaoClient import YinbaoClient
from . import const as c


class ProductsApi(YinbaoClient):

    def __init__(self, app_id, app_key, proxy=None):
        super().__init__(app_id, app_key, proxy=proxy)

    def get_products(self, post_back_param: dict = None):
        params = {
            'appId': self.app_id
        }
        if post_back_param:
            params['postBackParameter'] = post_back_param
        return self.request_with_params(c.POST, c.PRODUCTS, params)