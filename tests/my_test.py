from app.crawler import MyCrawlSpiderBuilder
from tests import BasicsTestCase
from app.tasks import start_my_crawl, start_my_crawl_dict


class MyTest(BasicsTestCase):

    def test_spider(self):
        name = 'hello'
        url = 'http://127.0.0.1:5000'
        builder = MyCrawlSpiderBuilder(name)\
            .add_start_url(url)
        # builder.add_link_rule('127.0.0.1', True)
        # start_my_crawl.delay(builder)
        start_my_crawl_dict.delay(builder.to_dict())