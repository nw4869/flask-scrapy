# encoding: utf-8

__author__ = 'nightwind'

import unittest
from app.models import *
from flask import current_app, url_for
from app import create_app, db
from app.crawler import MyCrawlSpiderBuilder
from app.tasks import start_my_crawl_dict


class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_new_task_and_config(self):
        name = 'test_task'
        start_url = 'http://utsc.guet.edu.cn/notice.aspx?mCode=001201'
        url_rule = 'noticeShow.asp'
        tag_title = u'(?<=<span id="lbTitle">).*?(?=</span>)'
        tag_clicks = u'(?<=<span id="lbHits">点击数：).*?(?=</span>'
        # new task
        task = Task(name=name)
        db.session.add(task)
        db.session.commit()
        self.assertEqual(task.name, name)
        self.assertEqual(task.id, 1)

        # add start url and url rule
        task.urls.append(Url(rule1=start_url))
        task.urls.append(Url(rule1=url_rule, type=1))
        db.session.commit()
        self.assertEqual(task.urls.count(), 2)

        # add tags
        task.tags.append(Tag(name='title', rule1=tag_title))
        task.tags.append(Tag(name='clicks', rule1=tag_clicks))
        db.session.commit()
        self.assertEqual(task.tags.filter(Tag.name=='clicks').one().rule1, tag_clicks)

        # start task
        builder = MyCrawlSpiderBuilder(task.name, task.id)
        for url in task.urls:
            if url.type == 0:
                builder.add_start_url(url.rule1)
            elif url.type == 1:
                builder.add_link_rule(url.rule1)
        for tag in task.tags:
            builder.add_tags(tag.id, tag.rule1)
        start_my_crawl_dict.delay(builder.to_dict())

    def test_new_tag(self):
        task = Task(name="the task")
        db.session.add(task)
        db.session.commit()
        tag_name = u'name1111'
        response = self.client.post(url_for('task.new_tag', task_id=task.id), data={
            'name': tag_name,
            'type': u'0',
            'rule1': u'rule111111'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(task.tags.one().name, tag_name)
