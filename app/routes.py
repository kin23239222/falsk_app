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