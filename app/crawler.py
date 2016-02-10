from scrapy.settings import Settings

__author__ = 'nightwind'

import scrapy
from scrapy.crawler import CrawlerProcess, Crawler
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from billiard import Process
import re


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
        settings = Settings()
        settings.set('ITEM_PIPELINES', {
            'app.pipelines.JsonWriterPipeline': 300
        })
        self.process = CrawlerProcess(settings)
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
    def __init__(self, name=None, task_id=None, start_urls=None, rules=None, builder=None, *a, **kw):
        if builder is not None:
            self.name = builder.name
            self.start_urls = builder.start_urls
            self.pre_rules = builder.rules
            self.tags = builder.tags
            self.task_id = builder.task_id
        else:
            self.name = name
            self.start_urls = start_urls
            self.pre_rules = rules
            self.task_id = task_id
        self.__init_rules()
        super(MyCrawlSpider, self).__init__(*a, **kw)

    def __init_rules(self):
        rules = []
        print('***********rules:', self.pre_rules)
        for rule in self.pre_rules:
            url = rule[0].encode('utf-8')
            follow = rule[1]
            if follow:
                rules.append(Rule(LinkExtractor(allow=(url,)), callback='parse_item'))
                print('*********add url', url)
            else:
                rules.append(Rule(LinkExtractor(deny=(url,))))
        self.rules = tuple(rules)
        print('**************rules:', self.rules)

    def parse_item(self, response):
        print('*********parse_item ... for ', response)
        # print('******response.body', response.body.decode(response.encoding))
        item = MyItem()
        # item['test_key'] = 'test_vaule'
        # data = response.decode(response.encoding)

        # TODO fix encode and regex

        item['task_id'] = self.task_id
        item['url'] = response.url.encode('utf-8')
        item['my_item'] = []
        print('*********tags', self.tags)
        html_doc = response.body.decode('utf-8')
        for tag in self.tags:
            try:
                result = re.search(tag[1], html_doc, re.S|re.U)
                if result is not None:
                    print('result = ',result.group()[:100])
                    result = result.group()
                else:
                    result = ''
                    print('result is none')
                print('***********data', result[:100])
            except :
                result = ''
            # item['my_item'].append((tag[0], result.encode('utf-8')))
            item['my_item'].append((tag[0], result))
        return item


class MyItem(scrapy.Item):
    my_item = scrapy.Field()
    task_id = scrapy.Field()
    url = scrapy.Field()


class MyCrawlSpiderBuilder:
    def __init__(self, name, task_id):
        self.name = name
        self.task_id = task_id
        self.start_urls = []
        self.rules = []
        self.tags = []

    def add_start_url(self, url):
        self.start_urls.append(url)
        return self

    def add_tags(self, tag_id, rule1):
        self.tags.append((tag_id, rule1))

    def add_link_rule(self, url, follow=True):
        self.rules.append((url, follow))
        return self

    def build(self):
        return MyCrawlSpider(self.name, self.start_urls, self.rules)

    def to_dict(self):
        return {'name': self.name, 'start_urls': self.start_urls, 'rules': self.rules, 'tags': self.tags,
                'task_id': self.task_id}

    def from_dict(self, builder_dict):
        self.name = builder_dict['name']
        self.start_urls = builder_dict['start_urls']
        self.rules = builder_dict['rules']
        self.tags = builder_dict['tags']
        self.task_id = builder_dict['task_id']


if __name__ == '__main__':
    # MySpiderProcess('asdf', ['http://baidu.com']).start()
    builder = MyCrawlSpiderBuilder('hello')
    builder.add_start_url('http://baidu.com')

    process = CrawlerProcess()
    process.crawl(MyCrawlSpider, builder=builder)
    process.start()
    pass
