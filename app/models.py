from datetime import datetime, timedelta

import pytz

from . import db  # 相对导入，获取在 __init__.py 中初始化的 SQLAlchemy 实例
from sqlalchemy import Column, DateTime

"""
作用：
定义数据库表结构（如 Task 表）。
由 SQLAlchemy ORM 管理，支持 CRUD 操作。

特点：
每个类对应一张表，每个字段对应数据库列。
配合 Flask-Migrate 实现数据库迁移。
"""


def beijing_now():
    """
    转化为北京时间
    :return:
    """
    return datetime.utcnow() + timedelta(hours=8)

# -----------------------------
# 定义模型
# -----------------------------
class Task(db.Model):


    __tablename__ = 'flask_list'  # 已存在的表
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250), nullable=False)
    done = db.Column(db.Boolean, default=False)
    date = db.Column(db.DateTime, default=beijing_now)
    date_inform = db.Column(db.DateTime, default=beijing_now)

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'done': self.done,
                'date': self.date.strftime('%Y-%m-%d %H:%M') if self.date else None,
                'date_inform': self.date_inform.strftime('%Y-%m-%d %H:%M') if self.date_inform else None
                }

    def __repr__(self):
        return f'<Task {self.name}, done={self.done}>'

