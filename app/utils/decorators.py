import functools
import time
import logging

logger = logging.getLogger(__name__)


def retry(max_retries=5, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.info(f"Error occurred in {func.__name__}: {e}. Retrying {retries + 1}/{max_retries}...")
                    retries += 1
                    time.sleep(delay)
            logger.info(f"Failed to execute {func.__name__} after {max_retries} attempts.")
        return wrapper
    return decorator