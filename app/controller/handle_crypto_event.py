from app.config import Config
from app.services.message_service import MessageService
from datetime import datetime, timedelta
from app.feishu.FeishuAppRobot import FeishuAppRobot
from app.models.balance import Balance
from app.models.bills_history import BillsHistory
from app.models.deposit_history import DepositHistory
from app.models.withdraw_history import WithdrawHistory
from app.models.instruments import Instruments
from app.models.mark_price import MarkPrice
from app.models.positions import Positions
from app.services.sync_service import SyncService
from app.services.crypto_report import CryptoReportService
from app.services.risk_report import RiskReportService
import time


def handle_crypto_update():
    receive_id = Config.get_user_id('Fang Yongchao')
    msg_service = MessageService(FeishuAppRobot(**Config.get_crypto_robot()))

    msg_service.send_text_message(receive_id=receive_id, content='Starting data update')
    start_time = (datetime.now() - timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')
    start_time = int(time.mktime(time.strptime(start_time, '%Y-%m-%d %H:%M:%S')) * 1000)

    tasks = [
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
    for task_type, table_class, strategy, *extra_params in tasks:
        try:
            additional_args = extra_params[0] if extra_params else {}
            if task_type == 'single':
                SyncService.update_table(table_class, strategy, **additional_args)
                msg_service.send_text_message(
                    receive_id=receive_id,
                    content=f'{table_class.__tablename__} updated {additional_args}'
                )
            elif task_type == 'multiple':
                SyncService.update_multiple_table(table_class, strategy, **additional_args)
                msg_service.send_text_message(
                    receive_id=receive_id,
                    content=f'{table_class.__tablename__} updated {additional_args}'
                )
        except Exception as e:
            msg_service.send_text_message(receive_id=receive_id, content=f'Error updating {table_class.__tablename__}: {str(e)}')

    msg_service.send_text_message(receive_id=receive_id, content='Data update completed')


def handle_crypto_report():
    receive_id = Config.get_user_id('Fang Yongchao')
    msg_service = MessageService(FeishuAppRobot(**Config.get_crypto_robot()))
    crs = CryptoReportService()

    msg_service.send_text_message(receive_id=receive_id, content='Finance Report Generating')

    msg_service.send_interactive_card(
        receive_id=receive_id, template_id=crs.id, template_variable=crs.report(),
        template_version_name=crs.version_name
    )


def handle_risk_report():
    receive_id = Config.get_user_id('Fang Yongchao')
    msg_service = MessageService(FeishuAppRobot(**Config.get_crypto_robot()))

    msg_service.send_text_message(receive_id=receive_id, content='Risk Report Generating')

    msg_service.send_interactive_card(
        receive_id=receive_id, template_id=RiskReportService.id, template_variable=RiskReportService.report(),
        template_version_name=RiskReportService.version_name
    )