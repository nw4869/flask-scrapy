__author__ = 'nightwind'

from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from celery import Celery
from config import config, Config
import celery_config

bootstrap = Bootstrap()
db = SQLAlchemy()
# celery = Celery(__name__, broker='redis://localhost:6379/0')
celery = Celery(__name__, broker=Config.CELERY_BROKER_URL, backend=Config.CELERY_RESULT_BACKEND)
celery.config_from_object('app.celery_config')

from project.views import do_sth


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    celery.conf.update(app.config)

    bootstrap.init_app(app)
    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .project import pj as project_blueprint
    app.register_blueprint(project_blueprint, url_prefix='/project')

    return app
