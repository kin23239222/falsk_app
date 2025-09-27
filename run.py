# run.py
from app import create_app

"""
作用：
本地开发调试启动脚本。
调用 create_app() 创建 app，然后用 Flask 内置服务器运行。

特点：
可设置 debug=True、模板自动刷新等。
开发环境用，生产环境不用。
"""


# 创建 Flask app 实例
app = create_app("DevConfig")

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",  # 外网访问可用
        port=5000,       # 开发环境端口
        debug=True       # 自动开启调试模式
    )
