from abc import ABC, abstractmethod
from datetime import datetime as dt
from app.utils.decorators import retry


class DataFetcher(ABC):
    def __init_subclass__(cls):
        """
        在子类被初始化时，自动为子类的 fetch_dat 方法添加 retry 装饰器
        """
        super().__init_subclass__()
        original_fetch_data = cls.fetch_data

        # 使用装饰器重新定义 fetch_dat 方法
        @retry(max_retries=3, delay=2)
        def wrapped_fetch_dat(self, **kwargs):
            return original_fetch_data(self, **kwargs)

        cls.fetch_dat = wrapped_fetch_dat

    @abstractmethod
    def fetch_data(self, **kwargs):
        pass

    @abstractmethod
    def process_data(self, **kwargs):
        pass

    @staticmethod
    def process_keys(item, key_mapping):
        return {
            key_mapping[k]: None if v in ['', '-'] else v
            for k, v in item.items()
            if k in key_mapping
        }

    @staticmethod
    def from_timestamp(x):
        try:
            result = dt.fromtimestamp(int(x) / 1000)
        except ValueError:
            result = None
        return result