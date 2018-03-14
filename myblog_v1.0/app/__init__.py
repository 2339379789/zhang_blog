from flask import Flask, render_template
from .config import config
from .extensions import config_extensions
from app.views import config_blueprint


# 封装一个函数，专门来创建APP
def create_app(config_name):
    # 创建实例
    app = Flask(__name__)
    # 通过对象初始化
    app.config.from_object(config[config_name])
    # 调用初始化方法
    config[config_name].init_app(app)
    # 配置各种扩展
    config_extensions(app)
    # 配置蓝本
    config_blueprint(app)
    # 配置错误页面
    config_errorhandler(app)
    # 返回实例
    return app


# 定制错误页面
def config_errorhandler(app):
    @app.errorhandler(404)
    def pag_not_found(e):
        return render_template('errors/404.html')
