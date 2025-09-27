from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
'''
作用：统一声明第三方扩展实例（如 SQLAlchemy、Flask-Migrate）。
特点：
只声明实例对象，不绑定 app，不管环境。
在 __init__.py 里通过 init_app(app) 绑定到 Flask app。
优点：项目结构清晰，扩展实例可在多个模块共享。
'''

db = SQLAlchemy()
migrate = Migrate()