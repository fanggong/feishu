import functools
import time


def retry(max_retries=5, delay=1, exceptions=(Exception,)):
    """
    一个重试装饰器，用于在发生指定异常时进行重试。
    :param max_retries: 最大重试次数
    :param delay: 每次重试的延迟时间（秒）
    :param exceptions: 需要捕获的异常类型（可以是一个元组）
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    retries += 1
                    print(f"Error occurred in {func.__name__}: {e}. Retrying {retries}/{max_retries}...")
                    time.sleep(delay)
            print(f"Failed to execute {func.__name__} after {max_retries} attempts.")
        return wrapper
    return decorator
