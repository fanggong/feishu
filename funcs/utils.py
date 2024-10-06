from datetime import datetime as dt
import pandas as pd


def from_timestamp(x):
    try:
        result = dt.fromtimestamp(int(x) / 1000)
    except BaseException:
        result = None
    return result


def format_number(value, decimals):
    # 使用格式化字符串指定小数位数，格式化为指定的小数位数
    format_str = f"{{:.{decimals}f}}"
    return format_str.format(value)


if __name__ == '__main__':
    print(format_number(3.2, 6))
