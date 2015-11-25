__author__ = 'nightwind'

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from billiard import Process


class MySpider1(scrapy.Spider):
    name = 'baidu'
    start_urls = ['http://baidu.com']

    def parse(self, response):
        print('hello world')


class MySpiderProcess1(scrapy.Spider):
    def __init__(self, name, urls):
        self.name = name
        self.start_urls = urls
        scrapy.Spider.__init__(self)

    def parse(self, response):
        print('parse response')

    def _crawl(self):
        self.process = CrawlerProcess()
        self.process.crawl(self, self.name, self.start_urls)
        self.process.start()
        # self.process.stop()
        # self.process.join()

    def start(self):
        p = Process(target=self._crawl)
        p.start()
        p.join()

    #
    # def start(self):
    #     self._crawl()

    def stop(self):
        self.process.stop()


class Parser:
    def __init__(self, callback):
        self.callback = callback

    def parse(self, response):
        self.callback(None)


class XPathParser(Parser):
    def __init__(self, xpath, callback):
        Parser.__init__(self, callback)
        self.xpath = xpath

    def parse(self, response):
        self.callback(response.xpath(self.xpath).extract())


class Item:
    def __init__(self, name, parser):
        self.name = name
        self.parser = parser

    def parse(self, response):
        self.parser.parse(response, self.parser_callback)

    def parser_callback(self, result):
        # TODO save to db
        print(result)


class ParserSpiderProcess1(MySpiderProcess1):
    def __init__(self, name, urls, items):
        super(ParserSpiderProcess1, self).__init__(name, urls)
        self.items = items


class MyCrawlSpider(CrawlSpider):
    def __init__(self, name=None, start_urls=None, rules=None, builder=None, *a, **kw):
        if builder is not None:
            self.name = builder.name
            self.start_urls = builder.start_urls
            self.rules = builder.rules
        else:
            self.name = name
            self.start_urls = start_urls
            self.rules = rules
        super(MyCrawlSpider, self).__init__(*a, **kw)


class MyCrawlSpiderBuilder:
    def __init__(self, name):
        self.name = name
        self.start_urls = []
        self.rules = []

    def add_start_url(self, url):
        self.start_urls.append(url)
        return self

    def add_link_rule(self, url, follow=True):
        if follow:
            self.rules.append(Rule(LinkExtractor(allow=(url,))))
        return self

    def build(self):
        return MyCrawlSpider(self.name, self.start_urls, self.rules)


if __name__ == '__main__':
    # MySpiderProcess('asdf', ['http://baidu.com']).start()
    builder = MyCrawlSpiderBuilder('hello')
    builder.add_start_url('http://baidu.com')

    process = CrawlerProcess()
    process.crawl(MyCrawlSpider, builder=builder)
    process.start()
    pass
