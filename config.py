# coding=utf-8
__author__ = 'nightwind'
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # celery
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL') or "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND') or "redis://localhost:6379/0"

    BABEL_DEFAULT_LOCALE = 'zh_Hans_CN'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    # WTF_CSRF_ENABLED = False
    DEBUG = True
    # DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    # 加载bootstrap本地css与js文件
    BOOTSTRAP_SERVE_LOCAL = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
    # 'default': ProductionConfig
}
