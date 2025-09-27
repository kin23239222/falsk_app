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


def create_app():
    app = Flask(__name__)

    # 从系统环境变量读取当前环境，默认为开发环境
    env = os.getenv("FLASK_ENV", "development")
    if env == "production":
        # 生产环境配置
        app.config.from_object("config.ProdConfig")
    else:
        # 开发环境配置
        app.config.from_object("config.DevConfig")

    # 初始化数据库和迁移工具
    db.init_app(app)
    migrate.init_app(app, db)

    # 导入路由和模型
    with app.app_context():
        from . import routes, models

    return app
