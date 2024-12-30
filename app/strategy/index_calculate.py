import pandas as pd
from ta.trend import sma_indicator, macd, macd_signal
from ta.momentum import rsi
from ta.volatility import BollingerBands
from . import const as c


def ma5(df):
    df.loc[:, c.MA5] = sma_indicator(df['close'], window=5)
    return df

def ma20(df):
    df.loc[:, c.MA20] = sma_indicator(df['close'], window=20)
    return df

def ma50(df):
    df.loc[:, c.MA50] = sma_indicator(df['close'], window=50)
    return df

def rsi14(df):
    df['rsi14'] = rsi(df['close'], window=14)
    return df

def macd_(df):
    df['macd'] = macd(df['close'])
    df['macd_signal'] = macd_signal(df['close'])
    return df

def boll_band(df):
    boll = BollingerBands(df['close'], window=20, window_dev=2)
    df.loc[:, c.BOLL_UP] = boll.bollinger_hband()
    df.loc[:, c.BOLL_DOWN] = boll.bollinger_lband()
    df.loc[:, c.BOLL] = boll.bollinger_mavg()
    return df

