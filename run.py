from app.main import app
from app.services.message_service import MessageService
from app.feishu.FeishuAppRobot import FeishuAppRobot
from app.config import Config
from app.controller.handle_bar_event import handle_bar_update
from app.controller.handle_crypto_event import handle_crypto_update
from app.models.tickets import Tickets
from app.repositories.query_repository import QueryRepository
from app.repositories.update_repository import UpdateRepository
from app.services.update_strategy import UpdateStrategy
from app.controller.handle_crypto_event import CryptoReportService
from app.models.balance import Balance
from app.models.bills_history import BillsHistory
from app.services.sync_service import SyncService
from app.models.products import Products
from app.models.instruments import Instruments
from app.models.deposit_history import DepositHistory
from datetime import datetime, timedelta
import time


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=11066)
    # start_time = (datetime.now() - timedelta(hours=24)).strftime('%Y-%m-%d %H:%M:%S')
    # start_time = int(time.mktime(time.strptime(start_time, '%Y-%m-%d %H:%M:%S')) * 1000)
    # SyncService.update_table(BillsHistory, BillsHistory.update_strategy, begin=start_time)
    # SyncService.update_table(DepositHistory, DepositHistory.update_strategy)
    # SyncService.update_table(Instruments, Instruments.update_strategy, instType='SPOT')
    SyncService.update_table(Products, Products.update_strategy)
