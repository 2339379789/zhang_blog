import os

base_dir = os.path.abspath(os.path.dirname(__file__))


class Config():
    # 秘钥
    SECRET_KEY = os.environ.get('SECRET_KEY') or '123456'
    # 数据库
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 邮件发送
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.163.com'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or '17165730064@163.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'ZWM123456'
    # 使用本地bootstrap库
    BOOTSTRAP_SERVE_LOCAL = True
    # 模板文件修改后自动加载
    TEMPLATES_AUTO_RELOAD = True
    # 上传文件配置
    # 上传文件的大小
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024
    # 上传文件的路径
    UPLOADED_PHOTOS_DEST = os.path.join(base_dir, 'static/upload')

    # 初始化函数，完成特定环境的初始化
    @staticmethod
    def init_app(app):
        pass


# 开发环境的配置
class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'blog-dev.sqlite')


# 测试环境配置
class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'blog-test.sqlite')


# 生产环境配置
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'blog.sqlite')
    MAIL_PORT = 465
    MAIL_USE_SSL = True


# 配置环境字典
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    # 默认环境
    'default': DevelopmentConfig
}
