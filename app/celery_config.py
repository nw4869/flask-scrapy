from kombu import serialization
from config import basedir, Config
import os
serialization.registry._decoders.pop("application/x-python-serialize")

BROKER_URL = Config.CELERY_BROKER_URL
RESULT_BACKEND = Config.CELERY_RESULT_BACKEND
# BROKER_URL = 'sqla+sqlite:///' + os.path.join(basedir, 'celerydb.sqlite')

CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']  # Ignore other content
CELERY_RESULT_SERIALIZER = 'json'

