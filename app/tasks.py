__author__ = 'nightwind'

from celery import Celery
from config import Config
from crawler import MySpiderProcess

celery = Celery(__name__, broker=Config.CELERY_BROKER_URL, backend=Config.CELERY_RESULT_BACKEND)


@celery.task
def start_crawl(name, urls):
    MySpiderProcess(name, urls).start()
    print('start spider')
    return {'result': 'ok'}
    # return 'ok'


@celery.task
def do_sth():
    print('do sth')
