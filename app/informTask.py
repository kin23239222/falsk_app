from datetime import datetime

from .models import Task,db
import pytz as pytz
from .utiles import send_tg_message
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
        print(f"时间{now}")
        tasks = Task.query.filter_by(done=False).all()
        for task in tasks:
            if task.date_inform is not None:
                task_time = tz.localize(task.date_inform) if task.date_inform.tzinfo is None else task.date_inform
                if task_time <= now:
                    send_tg_message(f"任务提醒：{task.name}")
                    task.done = True
        db.session.commit()


def init_scheduler(app):
    # 传入 app 给 check_tasks
    scheduler.add_job(check_tasks, 'interval', minutes=1, args=[app])
    scheduler.start()