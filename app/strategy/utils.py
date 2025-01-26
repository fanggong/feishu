import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from .const import *


def update_last_row(df: pd.DataFrame, new_row: list):
    assert len(new_row) == 6, 'new_row 的长度必须为 6'
    columns_to_update = ['ts', 'open', 'high', 'low', 'close', 'confirm']
    new_row = [float(value) for value in new_row]
    df.loc[df.index[-1], columns_to_update] = new_row
    return df[columns_to_update]

def insert_last_row(df: pd.DataFrame, new_row: list):
    assert len(new_row) == 6, 'new_row 的长度必须为 6'
    columns_to_update = ['ts', 'open', 'high', 'low', 'close', 'confirm']
    new_row = [float(value) for value in new_row]
    df = df.iloc[1:]
    new_row_data = {col: val for col, val in zip(columns_to_update, new_row)}
    df = pd.concat([df, pd.DataFrame([new_row_data])], ignore_index=True)
    return df[columns_to_update]

def generate_kline_figure(candles, indexes):
    # 获取candles字典的长度，决定子图的数量
    num_subplots = len(candles)

    # 创建一个纵向布局的子图，行数为candles的长度，列数为1
    fig = make_subplots(
        rows=num_subplots, cols=2, shared_xaxes=False,
        vertical_spacing=0.3 / num_subplots, horizontal_spacing=0.03, column_widths=[0.7, 0.3],
        specs=[[{'type': 'scatter'}, {'type': 'table'}]] * num_subplots,
        subplot_titles=[item for sublist in zip(candles.keys(), [''] * num_subplots) for item in sublist]
    )

    # 为每个子图添加一个K线图
    for i, (key, df) in enumerate(candles.items()):
        # 将时间戳转化为datetime格式
        df['time'] = pd.to_datetime(df['ts'].astype(int), unit='ms', utc=True).dt.tz_convert('Asia/Shanghai')
        df['customdata'] = list(zip(df['open'], df['high'], df['low'], df['close']))

        # 添加K线图
        fig.add_trace(go.Candlestick(
            x=df['time'],
            open=df['open'], high=df['high'], low=df['low'], close=df['close'],
            increasing=dict(fillcolor=INCREASING_COLOR, line=dict(color=INCREASING_COLOR)),
            decreasing=dict(fillcolor=DECREASING_COLOR, line=dict(color=DECREASING_COLOR)),
            customdata=df['customdata'],  # 自定义数据
            hoverinfo='text',  # 设置 hover 显示为自定义文本
            text=[
                f"OPEN: {row['open']}<br>"
                f"HIGH: {row['high']}<br>"
                f"LOW: {row['low']}<br>"
                f"CLOSE: {row['close']}"
                for _, row in df.iterrows()
            ]
        ), row=i + 1, col=1)

        # 添加指标曲线
        for index in indexes:
            if index in df.columns:
                fig.add_trace(go.Scatter(
                    x=df['time'],
                    y=df[index],
                    mode='lines',
                    name=index.upper(),
                    line=dict(color=index_color[index], width=1.5)
                ), row=i + 1, col=1)

        # 添加数据
        index = ['time', 'open', 'high', 'low', 'close'] + indexes
        value = df.iloc[-1][index]
        value.iloc[0] = value.iloc[0].strftime('%Y-%m-%d %H:%M:%S')
        value.iloc[1:] = value.iloc[1:].apply(lambda x: f"{{:.{6}f}}".format(x))
        fig.add_trace(
            go.Table(
                header=dict(
                    values=['INDEX', 'VALUE'],
                    font=dict(size=12),
                    align='center',
                ),
                cells=dict(
                    values=[[each.upper() for each in index], value],
                    align='left'
                ),
                columnwidth=[0.3, 0.7]
            ), row=i + 1, col=2
        )

        # 设置每个子图的x轴标题
        fig.update_xaxes(
            title_text='Time',
            rangeslider_visible=False,
            row=i + 1, col=1
        )

        # 设置每个子图的y轴标题
        fig.update_yaxes(
            title_text='Price',
            row=i + 1, col=1
        )


    # 更新布局
    fig.update_layout(
        height=400 * num_subplots,
        hovermode='x unified',  # 在x轴范围内对齐悬停
        showlegend=False
    )

    return fig
