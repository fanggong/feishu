from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit
from app.services.tasks import Tasks
from app.services.sync_service import SyncService


def sync_crypto_task():
    tasks = Tasks.get_crypto_update_tasks()
    for task_type, table_class, strategy, *extra_params in tasks:
        additional_args = extra_params[0] if extra_params else {}
        if task_type == 'single':
            SyncService.update_table(table_class, strategy, **additional_args)
        elif task_type == 'multiple':
            SyncService.update_multiple_table(table_class, strategy, **additional_args)


def sync_bar_task():
    tasks = Tasks.get_bar_update_tasks()
    for task_type, table_class, strategy, *extra_params in tasks:
        additional_args = extra_params[0] if extra_params else {}
        if task_type == 'single':
            SyncService.update_table(table_class, strategy)
        elif task_type == 'multiple':
            SyncService.update_multiple_table(table_class, strategy, **additional_args)


# 配置调度器
scheduler = BackgroundScheduler()
scheduler.start()


scheduler.add_job(
    func=sync_crypto_task,
    trigger=IntervalTrigger(minutes=20),
    id='crypto data',
    replace_existing=True
)

scheduler.add_job(
    func=sync_bar_task(),
    trigger=IntervalTrigger(hours=1),
    id='bar data',
    replace_existing=True
)

# 在程序退出时关闭调度器
atexit.register(lambda: scheduler.shutdown())
