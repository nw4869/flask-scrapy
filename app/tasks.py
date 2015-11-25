__author__ = 'nightwind'

from celery import Celery
from config import Config
from scrapy.crawler import CrawlerProcess
from crawler import MySpiderProcess1, MyCrawlSpider

celery = Celery(__name__, broker=Config.CELERY_BROKER_URL, backend=Config.CELERY_RESULT_BACKEND)


@celery.task
def start_crawl(name, urls):
    MySpiderProcess1(name, urls).start()
    print('start spider')
    return {'result': 'ok'}
    # return 'ok'


@celery.task
def do_sth():
    print('do sth')


@celery.task
def start_my_crawl(builder):
    process = CrawlerProcess()
    process.crawl(MyCrawlSpider, builder=builder)
    process.start()