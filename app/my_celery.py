__author__ = 'nightwind'

from flask import Flask, jsonify
from celery import Celery
from crawler import MySpiderProcess1, MyCrawlSpider
from flask.ext.script import Manager, Shell
from scrapy.crawler import CrawlerProcess

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery = Celery(app.name)
celery.conf.update(app.config)
manager = Manager(app)


# @celery.task(name='app.my_celery.my_background_task')
@celery.task
def my_background_task(arg1, arg2):
    # some long running task here
    print('aaaaaaaaa')
    return arg1 + arg2


@celery.task(name='app.my_celery.start_crawl')
def start_crawl(name, urls):
    MySpiderProcess1(name, urls).start()
    print('my spider started')


@celery.task
def start_my_crawl(builder):
    process = CrawlerProcess()
    process.crawl(MyCrawlSpider, builder)
    process.start()


@app.route('/')
def index():
    my_background_task.delay(1, 2)
    # start_crawl('baidu', ['http://baidu.com'])
    # start_crawl.delay('baidu', ['http://baidu.com'])
    # for i in range(5):
    # start_crawl('baidu', ['http://baidu.com'])
    # start_crawl('baidu', ['http://baidu.com'])
    # MySpider('baidu', ['http://baidu.com']).start()
    return jsonify({'result': 'ok'})


if __name__ == '__main__':
    app.run(debug=True)
    # app.run()
    # index()
    # manager.run()
