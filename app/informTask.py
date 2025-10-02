from datetime import datetime

from .models import Task,db
import pytz as pytz
from .utiles import  wy_mail_send
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

def check_tasks(app):
    """
    当任务到时间时进行通知
    :return:
    """
    with app.app_context():
        tz = pytz.timezone('Asia/Shanghai')
        now = datetime.now(tz)  # 或者用你的时区
        tasks = Task.query.filter(Task.done == False, Task.inform == False).all()
        for task in tasks:
            if task.date_inform is not None:
                task_time = tz.localize(task.date_inform) if task.date_inform.tzinfo is None else task.date_inform
                if task_time <= now:
                    # 通过tg机器人通知
                    # send_tg_message(f"任务提醒：{task.name}")
                    wy_mail_send(f"任务提醒：{task.name}")
                    # 通过网易邮箱通知
                    task.inform = True
        db.session.commit()


def init_scheduler(app):
    # 传入 app 给 check_tasks
    scheduler.add_job(check_tasks, 'interval', minutes=1, args=[app])
    scheduler.start()