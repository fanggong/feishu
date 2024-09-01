import functools
import time


def retry(max_retries=5, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Error occurred in {func.__name__}: {e}. Retrying {retries + 1}/{max_retries}...")
                    retries += 1
                    time.sleep(delay)
            print(f"Failed to execute {func.__name__} after {max_retries} attempts.")
        return wrapper
    return decorator