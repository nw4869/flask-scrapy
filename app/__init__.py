__author__ = 'nightwind'

from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from celery import Celery
from config import config, Config
import celery_config
import custom_error_pages

bootstrap = Bootstrap()
db = SQLAlchemy()
# celery = Celery(__name__, broker='redis://localhost:6379/0')
celery = Celery(__name__, broker=Config.CELERY_BROKER_URL, backend=Config.CELERY_RESULT_BACKEND)
# celery = Celery(__name__)
celery.config_from_object('app.celery_config')

from task.views import do_sth


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    celery.conf.update(app.config)

    bootstrap.init_app(app)
    db.init_app(app)
    # with app.app_context():
        # Extensions like Flask-SQLAlchemy now know what the "current" app
        # is while within this block. Therefore, you can now run........
        # db.create_all()


    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .task import task as task_blueprint
    app.register_blueprint(task_blueprint, url_prefix='/task')

    app.error_handler_spec[None][404] = custom_error_pages.page_not_found
    app.error_handler_spec[None][500] = custom_error_pages.internal_server_error

    print('app create')

    return app
