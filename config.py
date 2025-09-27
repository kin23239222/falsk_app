import os  # 用于读取系统环境变量

from sqlalchemy import NullPool

"""
作用：集中管理项目的配置项（数据库、调试模式、模板刷新、密钥等）。

特点：
可以区分开发环境和生产环境。
通过环境变量控制加载不同配置。
典型配置包括：数据库 URI、SQLAlchemy 引擎选项、DEBUG、TEMPLATES_AUTO_RELOAD。
"""


# =========================================
# 基础配置类（所有环境都通用的配置）
# =========================================
class Config:
    # Flask 的密钥，用于 session 加密、表单 CSRF 等安全功能
    # 如果系统环境变量中有 SECRET_KEY，则使用，否则用默认值 "dev-secret-key"
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    # SQLAlchemy 配置项，关闭对象修改追踪，节省内存
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# =========================================
# 开发环境配置
# =========================================
class DevConfig(Config):
    # 开启调试模式，代码修改会自动重载，报错会显示详细信息
    DEBUG = True

    # 数据库 URI（开发环境用 SQLite）
    # 优先使用环境变量 DEV_DATABASE_URL，如果没有则用默认本地 SQLite 文件 dev.db
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DEV_DATABASE_URL", "mysql+pymysql://root:123456@localhost:3306/flask"
    )

    TEMPLATES_AUTO_RELOAD = True  # 开发环境模板自动刷新

# =========================================
# 生产环境配置
# =========================================
class ProdConfig(Config):
    # 生产环境关闭调试
    DEBUG = False

    # 数据库 URI（生产环境用 MySQL）
    # 优先使用环境变量 DATABASE_URL，否则用默认本地 MySQL
    # 格式: "mysql+pymysql://用户名:密码@主机/数据库名"
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "sqlite:///local.db"
    )
    TEMPLATES_AUTO_RELOAD = False  # 开发环境模板自动刷新
    # 新增：配置连接池选项（关键修复）
    SQLALCHEMY_ENGINE_OPTIONS = {
        'poolclass': NullPool,  # 禁用SQLAlchemy连接池，避免与Supabase冲突
        'pool_pre_ping': True,  # 连接前ping检测
    }
