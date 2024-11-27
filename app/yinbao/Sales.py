from .yinbaoClient import YinbaoClient
from . import const as c
from datetime import datetime, timedelta


class SalesApi(YinbaoClient):

    def __init__(self, app_id, app_key, proxy=None):
        super().__init__(app_id, app_key, proxy=proxy)

    def get_tickets(self, start_time, end_time, post_back_param: dict = None):
        params = {
            'appId': self.app_id,
            'startTime': start_time,
            'endTime': end_time,
            'noLimitTimeRange': 1
        }
        if post_back_param:
            params['postBackParameter'] = post_back_param
        return self.request_with_params(c.POST, c.TICKETS, params)
