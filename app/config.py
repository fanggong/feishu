import yaml


class Config:
    @classmethod
    def load_config(cls):
        with open('config.yml', 'r') as file:
            config = yaml.safe_load(file)
            return config

    @classmethod
    def get_mysql_url(cls):
        config = cls.load_config()['database']['mysql']
        return f"mysql+pymysql://{config['username']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"

    @classmethod
    def get_okx_keys(cls):
        config = cls.load_config()['okx']
        return {'api_key': config['api_key'], 'api_secret_key': config['secret_key'], 'passphrase': config['passphrase']}

    @classmethod
    def get_yinbao_keys(cls):
        config = cls.load_config()['yinbao']
        return {'app_id': config['app_id'], 'app_key': config['app_key']}

    @classmethod
    def get_crypto_robot(cls):
        config = cls.load_config()['feishu']['crypto']
        return {'app_id': config['app_id'], 'app_secret': config['app_secret'], 'name': config['name']}

    @classmethod
    def get_bar_robot(cls):
        config = cls.load_config()['feishu']['bar']
        return {'app_id': config['app_id'], 'app_secret': config['app_secret'], 'name': config['name']}

    @classmethod
    def get_user_id(cls, name):
        config = cls.load_config()['feishu_user_id']
        return config[name]