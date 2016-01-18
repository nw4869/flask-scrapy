__author__ = 'nightwind'

# from celery import Celery
from app import celery
from scrapy.crawler import CrawlerProcess, Settings
from crawler import MySpiderProcess1, MyCrawlSpider, MyCrawlSpiderBuilder


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
    settings = Settings()
    # settings.set('DEPTH_LIMIT', 1)
    settings.set("ITEM_PIPELINES", {
        # 'app.pipelines.JsonWriterPipeline': 200,
        'app.pipelines.DataBasePipeline': 300,
    })

    process = CrawlerProcess(settings)
    process.crawl(MyCrawlSpider, builder=builder)
    process.start()
    process.stop()


@celery.task
def start_my_crawl_dict(builder_dict):
    builder = MyCrawlSpiderBuilder(builder_dict['name'])
    builder.from_dict(builder_dict)
    start_my_crawl(builder)
