import time
from datetime import datetime, timedelta
from app.models import *


class Tasks:
    @staticmethod
    def get_crypto_update_tasks(start_time=None):
        # 默认更新过去一小时的数据
        if not start_time:
            start_time = (datetime.now() - timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')
            start_time = int(time.mktime(time.strptime(start_time, '%Y-%m-%d %H:%M:%S')) * 1000)
        return [
            ('single', Balance, Balance.update_strategy),
            ('single', BillsHistory, BillsHistory.update_strategy, {'begin': start_time}),
            ('single', DepositHistory, DepositHistory.update_strategy),
            ('single', WithdrawHistory, WithdrawHistory.update_strategy),
            # ('single', Instruments, Instruments.update_strategy, {'instType': 'SPOT'}),
            ('single', Instruments, Instruments.update_strategy, {'instType': 'SWAP'}),
            ('single', Instruments, Instruments.update_strategy, {'instType': 'MARGIN'}),
            ('single', MarkPrice, MarkPrice.update_strategy, {'instType': 'SWAP'}),
            ('single', MarkPrice, MarkPrice.update_strategy, {'instType': 'MARGIN'}),
            ('single', Positions, Positions.update_strategy)
        ]

    @staticmethod
    def get_bar_update_tasks(start_time=None, end_time=None):
        # 默认更新过去6小时的数据
        if not start_time:
            start_time = (datetime.now() - timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S')
        if not end_time:
            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return [
            ('single', Products, Products.update_strategy),
            ('single', Customers, Customers.update_strategy),
            ('multiple', Tickets, {Tickets: Tickets.update_strategy, TicketItems: TicketItems.update_strategy}, {'start_time': start_time, 'end_time': end_time})
        ]