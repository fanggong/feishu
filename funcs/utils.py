from datetime import datetime as dt


def from_timestamp(x):
    try:
        result = dt.fromtimestamp(int(x) / 1000)
    except BaseException:
        result = None
    return result