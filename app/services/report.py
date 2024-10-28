from abc import ABC, abstractmethod


class ReportService(ABC):
    @property
    @abstractmethod
    def id(self):
        pass

    @property
    @abstractmethod
    def version_name(self):
        pass

    @abstractmethod
    def report(self, **kwargs):
        pass

    @staticmethod
    def format_number(value, decimals=2):
        # 使用格式化字符串指定小数位数，格式化为指定的小数位数
        format_str = f"{{:.{decimals}f}}"
        return format_str.format(value)

