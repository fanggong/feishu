from .yinbaoClient import YinbaoClient
from . import const as c


class AccessApi(YinbaoClient):

    def __init__(self, app_id, app_key):
        super().__init__(app_id, app_key)

    def get_access_times(self):
        params = {
            'appId': self.app_id
        }
        return self.request_with_params(c.POST, c.ACCESS_TIMES, params)