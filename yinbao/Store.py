from .yinbaoClient import YinbaoClient
from . import const as c


class StoreApi(YinbaoClient):

    def __init__(self, app_id, app_key):
        super().__init__(app_id, app_key)

    def get_store_list(self):
        params = {
            'appId': self.app_id
        }
        return self.request_with_params(c.POST, c.STORE_LIST, params)