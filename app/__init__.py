# app/__init__.py
import os

from flask import Flask
from .extensions import db, migrate

"""
作用：
使用 工厂模式创建 Flask app 实例。
根据环境加载配置 (config.py)。
初始化扩展（extensions.py）和注册路由、模型。

特点：
生产和开发环境都用同一个入口。
是项目的核心“启动点”，但不是直接运行文件。
"""


def create_app(config_name="DevConfig"):
    app = Flask(__name__,
               static_url_path='/task/static',   # 静态文件访问 URL 前缀
            static_folder=os.path.join(os.path.dirname(__file__), 'static')
               )

    # 选择环境配置
    app.config.from_object(f"config.{config_name}")
    print("当前数据库:", app.config["SQLALCHEMY_DATABASE_URI"])

    # 初始化数据库和迁移工具
    db.init_app(app)
    migrate.init_app(app, db)

    # 注册路由和蓝图
    with app.app_context():
        from . import routes, models

        # 假设 routes.py 中有 blueprint = Blueprint('task', __name__)
        # 如果没有蓝图，可以直接使用 app.route，这里可以加 url_prefix
        # 如果你想统一用 /task/ 前缀，可以用蓝图
        try:
            from .routes import task_blueprint
            app.register_blueprint(task_blueprint, url_prefix='/task')
        except ImportError:
            pass

    return app