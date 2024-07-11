import requests


class Feishu:
    def __init__(self, app_id=None, app_secret=None):
        self.app_id = app_id
        self.app_secret = app_secret

        url = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/'
        post_data = {'app_id': app_id, 'app_secret': app_secret}
        r = requests.post(url, data=post_data)
        self.tenant_access_token = r.json()['tenant_access_token']
        print(f'tenant_access_token: {self.tenant_access_token}')
