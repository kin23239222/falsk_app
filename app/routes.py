import gc
import os
from collections import defaultdict
from .models import Task, db
from flask import current_app as app  # 获取当前 app 实例
import psutil
from flask import  render_template, request, jsonify

"""
作用：
定义 Flask URL 路由和处理函数（增删改查逻辑）。
渲染模板，处理前端请求。

特点：
只关注业务逻辑，不处理数据库连接初始化。
可以引用 models.py 和 extensions.py。
"""

# 获取 待执行 列表
@app.route('/')
def to_do_list():
    tasks = Task.query.filter(Task.done == False, Task.type == 0).all()
    return render_template("index.html", tasks=[t.to_dict() for t in tasks])

# 获取 按日期分组 列表
@app.route('/done')
def done():
    tasks = Task.query.filter_by(done=True).order_by(Task.date).all()
    task_by_date = defaultdict(list)
    for i in tasks:
        date_str = i.date.strftime('%Y-%m-%d') if i.date else '未指定日期'
        task_by_date[date_str].append(i.to_dict())

    tasks_by_date = dict(sorted(task_by_date.items()))
    return render_template('done.html', tasks_by_date=tasks_by_date)

# 获取 待加入 列表
@app.route('/wait')
def wait():
    tasks = Task.query.filter(Task.done == False, Task.type == 1).all()
    return render_template("wait.html", tasks=[t.to_dict() for t in tasks])

# 点击完成任务
@app.route('/del_li', methods=['POST'])
def del_li():
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

# 点击完成任务
@app.route('/join_list_task', methods=['POST'])
def join_list_task():
    try:
        task = request.json.get('taskId')
        task_data = Task.query.get(task)
        if task_data:
            task_data.type = 0
            db.session.commit()
            return {'status': 'ok'}
        return {'status': 'error', 'message': '操作失败'}, 400
    except Exception as e:
        db.session.rollback()  # 新增错误回滚
        return {'status': 'error', 'message': '服务器错误'}, 500

# 点击取消完成任务
@app.route('/udel_li', methods=['POST'])
def udel_li():
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

# 增加任务
@app.route('/add_li', methods=['POST'])
def add_li():
    try:
        taskInput = request.json.get('taskInput')
        taskTime = request.json.get('taskTime')
        taskType = request.json.get('taskType')
        if not taskInput:
            return jsonify({'status': 'error', 'message': '任务名不能为空'}), 400
        if not taskTime:
            return jsonify({'status': 'error', 'message': '任务名不能为空'}), 400

        existing = Task.query.filter_by(name=taskInput, done=False).first()
        if existing:
            return jsonify({'status': 'error', 'message': '任务已存在'}), 400

        new_task = Task(name=taskInput, done=False, date_inform=taskTime, type=taskType)
        db.session.add(new_task)
        db.session.commit()
        return jsonify({'status': 'ok', 'task': new_task.to_dict()})
    except Exception as e:
        db.session.rollback()  # 新增错误回滚
        return jsonify({'status': 'error', 'message': '服务器错误'}), 500

# 新增：健康检查端点（不影响现有功能）
@app.route('/health')
def health_check():
    try:
        db.session.execute('SELECT 1')
        return 'OK'
    except:
        return 'Database Error', 500