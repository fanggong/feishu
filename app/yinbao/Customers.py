from .yinbaoClient import YinbaoClient
from . import const as c


class CustomersApi(YinbaoClient):

    def __init__(self, app_id, app_key):
        super().__init__(app_id, app_key)

    def get_customers(self, post_back_param: dict = None):
        params = {
            'appId': self.app_id
        }
        if post_back_param:
            params['postBackParameter'] = post_back_param
        return self.request_with_params(c.POST, c.CUSTOMERS, params)