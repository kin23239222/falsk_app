import gc
import os
from collections import defaultdict
from datetime import datetime

import psutil
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.pool import NullPool  # 新增导入

app = Flask(__name__)
if os.environ.get("FLASK_ENV") == "development":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True

# # 配置 MySQL 数据库连接
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/flask?charset=utf8mb4'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 避免警告
# db = SQLAlchemy(app)

# class Task(db.Model):
#     __tablename__ = 'flask_list'  # 已存在的表
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String(250), nullable=False)
#     done = db.Column(db.Boolean, default=False)  # tinyint -> Boolean
#     date = db.Column(db.DateTime, default= datetime.utcnow)
#
#     # 将数据转为字典类型
#     def to_dict(self):
#         return {'id': self.id,'name':self.name,'done':self.done,'date':self.date.strftime('%Y-%m-%d %H:%M')}
#
#     def __repr__(self):
#         return f'<Task {self.name}, done={self.done}>'


# -----------------------------
# 配置 Supabase PostgreSQL 数据库
# -----------------------------
# 替换为你自己的 Supabase Host
# DB_HOST = "db.icckmzphswnptfhnichd.supabase.co"
# DB_PORT = "5432"
# DB_NAME = "flask"
# DB_USER = "postgres"
# DB_PASSWORD = "123456"

# SQLAlchemy PostgreSQL URI
# 优先用环境变量 DATABASE_URL（Render 上会配置）
# 本地开发可以 fallback 到 SQLite（可选）
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", "sqlite:///local.db"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 新增：配置连接池选项（关键修复）
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'poolclass': NullPool,  # 禁用SQLAlchemy连接池，避免与Supabase冲突
    'pool_pre_ping': True,   # 连接前ping检测
}

db = SQLAlchemy(app)

# 新增：简单内存检查函数
def check_memory():
    """简单内存检查，只在Render环境运行"""
    if os.environ.get('RENDER'):
        try:
            process = psutil.Process(os.getpid())
            memory_mb = process.memory_info().rss / 1024 / 1024
            if memory_mb > 400:  # 超过400MB时回收
                gc.collect()
        except:
            pass  # 忽略内存检查错误


# -----------------------------
# 定义模型
# -----------------------------
class Task(db.Model):
    __tablename__ = 'flask_list'  # 已存在的表
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250), nullable=False)
    done = db.Column(db.Boolean, default=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'done': self.done,
                'date': self.date.strftime('%Y-%m-%d %H:%M') if self.date else None}

    def __repr__(self):
        return f'<Task {self.name}, done={self.done}>'



# 首页：任务列表 - 只添加内存检查
@app.route('/')
def to_do_list():
    check_memory()  # 新增
    tasks = Task.query.filter_by(done=False).all()
    return render_template("index.html", tasks=[t.to_dict() for t in tasks])

# 点击完成任务 - 只添加内存检查和错误处理
@app.route('/del_li', methods=['POST'])
def del_li():
    check_memory()  # 新增
    try:
        task = request.json.get('taskId')
        task_data = Task.query.get(task)
        if task_data:
            task_data.done = True
            db.session.commit()
            return {'status': 'ok'}
        return {'status': 'error', 'message': '操作失败'}, 400
    except Exception as e:
        db.session.rollback()  # 新增错误回滚
        return {'status': 'error', 'message': '服务器错误'}, 500

# 点击取消完成任务 - 只添加内存检查和错误处理
@app.route('/udel_li', methods=['POST'])
def udel_li():
    check_memory()  # 新增
    try:
        task = request.json.get('taskId')
        task_data = Task.query.get(task)
        if task_data:
            task_data.done = False
            db.session.commit()
            return {'status': 'ok'}
        return {'status': 'error', 'message': '操作失败'}, 400
    except Exception as e:
        db.session.rollback()  # 新增错误回滚
        return {'status': 'error', 'message': '服务器错误'}, 500

# 增加任务 - 只添加内存检查和错误处理
@app.route('/add_li', methods=['POST'])
def add_li():
    check_memory()  # 新增
    try:
        task_name = request.json.get('task')
        if not task_name:
            return jsonify({'status': 'error', 'message': '任务名不能为空'}), 400

        existing = Task.query.filter_by(name=task_name, done=False).first()
        if existing:
            return jsonify({'status': 'error', 'message': '任务已存在'}), 400

        new_task = Task(name=task_name, done=False)
        db.session.add(new_task)
        db.session.commit()
        return jsonify({'status': 'ok', 'task': new_task.to_dict()})
    except Exception as e:
        db.session.rollback()  # 新增错误回滚
        return jsonify({'status': 'error', 'message': '服务器错误'}), 500

# 获取日期进行分组 - 只添加内存检查
@app.route('/done')
def done():
    check_memory()  # 新增
    tasks = Task.query.filter_by(done=True).order_by(Task.date).all()

    task_by_date = defaultdict(list)
    for i in tasks:
        date_str = i.date.strftime('%Y-%m-%d') if i.date else '未指定日期'
        task_by_date[date_str].append(i.to_dict())

    tasks_by_date = dict(sorted(task_by_date.items()))
    return render_template('done.html', tasks_by_date=tasks_by_date)

# 新增：健康检查端点（不影响现有功能）
@app.route('/health')
def health_check():
    try:
        db.session.execute('SELECT 1')
        return 'OK'
    except:
        return 'Database Error', 500

if __name__ == '__main__':
    app.run(debug=True)
