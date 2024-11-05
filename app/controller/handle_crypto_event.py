from app.config import Config
from app.services.message import Message
from app.services.tasks import Tasks
from app.feishu.FeishuAppRobot import FeishuAppRobot
from app.services.sync_service import SyncService
from app.services.crypto_report import CryptoReportService
from app.services.risk_report import RiskReportService


def handle_crypto_update():
    receive_id = Config.get_user_id('Fang Yongchao')
    msg_service = Message(FeishuAppRobot(**Config.get_crypto_robot()))

    msg_service.send_text_message(receive_id=receive_id, content='Starting data update')
    tasks = Tasks.get_crypto_update_tasks()

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
    msg_service = Message(FeishuAppRobot(**Config.get_crypto_robot()))
    crs = CryptoReportService()

    msg_service.send_text_message(receive_id=receive_id, content='Finance Report Generating')

    msg_service.send_interactive_card(
        receive_id=receive_id, template_id=crs.id, template_variable=crs.report(),
        template_version_name=crs.version_name
    )


def handle_risk_report():
    receive_id = Config.get_user_id('Fang Yongchao')
    msg_service = Message(FeishuAppRobot(**Config.get_crypto_robot()))
    rrs = RiskReportService()

    msg_service.send_text_message(receive_id=receive_id, content='Risk Report Generating')

    msg_service.send_interactive_card(
        receive_id=receive_id, template_id=rrs.id, template_variable=rrs.report(),
        template_version_name=rrs.version_name
    )