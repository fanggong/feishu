from app.main import app
from app.config import Config
from app.models import *
from app.services.message_service import MessageService
from app.services.log import LogService
from app.feishu.FeishuAppRobot import FeishuAppRobot
from app.controller.handle_bar_event import handle_bar_update
from app.controller.handle_crypto_event import handle_crypto_update
from app.repositories.query_repository import QueryRepository
from app.repositories.update_repository import UpdateRepository
from app.services.update_strategy import UpdateStrategy
from app.controller.handle_crypto_event import CryptoReportService
from app.services.sync_service import SyncService
from app.models.deposit_history import DepositHistory
from datetime import datetime, timedelta
from app.services.sales_report import SalesReportService
import time
import scheduler


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=11066)
    # LogService.record_update_logs(Products, 1)
    # start_time = (datetime.now() - timedelta(hours=24)).strftime('%Y-%m-%d %H:%M:%S')
    # start_time = int(time.mktime(time.strptime(start_time, '%Y-%m-%d %H:%M:%S')) * 1000)
    # SyncService.update_table(BillsHistory, BillsHistory.update_strategy, begin=start_time)
    # SyncService.update_table(DepositHistory, DepositHistory.update_strategy)
    # SyncService.update_table(Instruments, Instruments.update_strategy, instType='SPOT')
    # SyncService.update_table(Products, Products.update_strategy)
    # start_time = (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d %H:%M:%S')
    # end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # SyncService.update_multiple_table(
    #     Tickets, {Tickets: Tickets.update_strategy, TicketItems: TicketItems.update_strategy},
    #     start_time=start_time, end_time=end_time
    # )
    # receive_id = Config.get_user_id('Fang Yongchao')
    # msg_service = MessageService(FeishuAppRobot(**Config.get_bar_robot()))
    # srs = SalesReportService()
    #
    # msg_service.send_text_message(receive_id=receive_id, content='Sales Report Generating')
    #
    # msg_service.send_interactive_card(
    #     receive_id=receive_id, template_id=srs.id, template_variable=srs.report(),
    #     template_version_name=srs.version_name
    # )

