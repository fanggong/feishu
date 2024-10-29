from app.services.sync_service import SyncService
from app.services.message_service import MessageService
from app.models.products import Products
from app.models.customers import Customers
from app.models.tickets import Tickets
from app.models.ticket_items import TicketItems
from app.config import Config
from app.feishu.FeishuAppRobot import FeishuAppRobot
from datetime import datetime, timedelta
from app.services.sales_report import SalesReportService


def handle_bar_update():
    receive_id = Config.get_user_id('Fang Yongchao')
    msg_service = MessageService(FeishuAppRobot(**Config.get_bar_robot()))

    msg_service.send_text_message(receive_id=receive_id, content='Starting data update')
    start_time = (datetime.now() - timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S')
    end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    tasks = [
        ('single', Products, Products.update_strategy),
        ('single', Customers, Customers.update_strategy),
        ('multiple', Tickets, {Tickets: Tickets.update_strategy, TicketItems: TicketItems.update_strategy}, {'start_time': start_time, 'end_time': end_time})
    ]
    for task_type, table_class, strategy, *extra_params in tasks:
        try:
            additional_args = extra_params[0] if extra_params else {}
            if task_type == 'single':
                SyncService.update_table(table_class, strategy)
                msg_service.send_text_message(receive_id=receive_id, content=f'{table_class.__tablename__} updated')
            elif task_type == 'multiple':
                SyncService.update_multiple_table(table_class, strategy, **additional_args)
                msg_service.send_text_message(receive_id=receive_id, content=f'{table_class.__tablename__} updated')
        except Exception as e:
            msg_service.send_text_message(receive_id=receive_id, content=f'Error updating {table_class.__tablename__}: {str(e)}')

    msg_service.send_text_message(receive_id=receive_id, content='Data update completed')


def handle_sales_report():
    receive_id = Config.get_user_id('Fang Yongchao')
    msg_service = MessageService(FeishuAppRobot(**Config.get_bar_robot()))
    srs = SalesReportService()

    msg_service.send_text_message(receive_id=receive_id, content='Sales Report Generating')

    msg_service.send_interactive_card(
        receive_id=receive_id, template_id=srs.id, template_variable=srs.report(),
        template_version_name=srs.version_name
    )
