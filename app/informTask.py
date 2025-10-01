from datetime import datetime
from .models import Task,db
import pytz as pytz
from utiles import send_tg_message
from apscheduler.schedulers.background import BackgroundScheduler



def check_tasks():
    """
    当任务到时间时进行通知
    :return:
    """
    now = datetime.now(pytz.UTC)  # 或者用你的时区
    tasks = Task.query.filter(Task.date_inform <= now).all()
    for task in tasks:
        send_tg_message(f"任务提醒：{task.name}")
        # 如果只提醒一次，可以更新数据库避免重复提醒
        db.session.delete(task)  # 或者加个标记字段
        db.session.commit()

# 创建调度器
scheduler = BackgroundScheduler()
# 将任务放入调度器
scheduler.add_job(check_tasks, 'interval', minutes=1)