import json

from httpx import Client
from . import const as c, utils as u
import logging

logger = logging.getLogger(__name__)

class YinbaoClient(Client):

    def __init__(self, app_id, app_key, base_url=c.API_URL, proxy=None):
        super().__init__(base_url=base_url, http2=True, proxy=proxy)
        self.app_id = app_id
        self.app_key = app_key
        self.domain = base_url

    def _request(self, method, request_path, params):
        if method == c.GET:
            request_path = request_path + u.parse_params_to_str(params)
        timestamp = u.get_timestamp()
        body = json.dumps(params) if method == c.POST else ''
        sign = u.encrypt_to_md5_string(body, self.app_key)
        header = u.get_header(timestamp, sign)
        logger.debug(f'domain: {self.domain}')
        logger.debug(f'request path: {request_path}')
        logger.debug(f'body: {body}')
        response = None
        if method == c.GET:
            response = self.get(request_path, headers=header)
        elif method == c.POST:
            response = self.post(request_path, data=body, headers=header)
        return response.json()

    def request_without_params(self, method, request_path):
        return self._request(method, request_path, {})

    def request_with_params(self, method, request_path, params):
        return self._request(method, request_path, params)
