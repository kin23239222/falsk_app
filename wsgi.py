# wsgi.py
from app import create_app

"""
作用：
生产环境入口，给 Gunicorn 或 uWSGI 调用。
调用 create_app()，暴露 app 对象。

特点：
不负责调试和开发功能。
和 run.py 一样使用工厂函数，但专门用于生产部署。
"""

# 创建 Flask app 实例
app = create_app()

# 可选：运行调试模式（生产环境通常不要）
if __name__ == "__main__":
    app.run()
