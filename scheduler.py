from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit


def scheduled_task():
    print("This task runs every 20 minutes.")


# 配置调度器
scheduler = BackgroundScheduler()
scheduler.start()


# 添加任务：每 20 分钟执行一次
scheduler.add_job(
    func=scheduled_task,
    trigger=IntervalTrigger(seconds=10),
    id='my_20_minute_task',
    replace_existing=True
)

# 在程序退出时关闭调度器
atexit.register(lambda: scheduler.shutdown())
