__author__ = 'nightwind'

import os
from app import create_app, db
from app.models import Task, Tag, Url
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from app import celery
from celery.bin import worker
from celery.bin.celery import main as celery_main
from flask.ext.babel import Babel

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)
babel = Babel(app)
app.config['BABEL_DEFAULT_LOCALE'] = 'zh_Hans_CN'



def make_shell_context():
    return dict(app=app, db=db, Task=Task, Item=Tag, Url=Url)


manager.add_command("shell", Shell(make_shell_context()))
manager.add_command("db", MigrateCommand)


@manager.command
def celery_worker():
    return celery_main(['celery', 'worker', '-A app.tasks'])


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def celeryd():
    db.init_app(app)

    # celery_app = current_app._get_current_object()
    celery_app = celery

    celery_worker = worker.worker(app=celery_app)

    options = {
        # 'broker': 'amqp://guest:guest@localhost:5672//',
        # 'loglevel': 'INFO',
        # 'traceback': True,
        # 'concurrency': 0
    }

    celery_worker.run(**options)


if __name__ == '__main__':
    manager.run()
    # app.run()
