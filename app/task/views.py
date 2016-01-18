# coding=utf-8
from billiard import Process

__author__ = 'nightwind'

from flask import render_template, flash, redirect, url_for
from . import task
from ..models import Task, Tag, Url, Item
from .forms import NewTaskForm
from ..tasks import do_sth, start_crawl, start_my_crawl, start_my_crawl_dict
from .. import db
from time import sleep
from ..crawler import MyCrawlSpider, MyCrawlSpiderBuilder


@task.route('/')
def index():
    # start_crawl.delay('baidu', ['http://baidu.com'])
    task = do_sth.delay()
    sleep(0.1)
    print(task.ready())

    print(task.status)

    tasks = Task.query.all()
    return render_template("task/index.html", tasks=tasks)


@task.route('/id/<task_id>/item/<item_id>')
def item_detail(task_id, item_id):
    # TODO 待完善
    try:
        # TODO 为什么过滤task无效
        item = Item.query.join(Tag).filter(Tag.task_id == task_id).filter(Item.id == item_id).one()
        return item.data
    except:
        pass
    return 'Not found', 404


@task.route('/id/<task_id>')
def detail(task_id):
    task = db.session.query(Task).filter(Task.id == task_id).first()
    tags = Tag.query.filter(Tag.task == task).all()

    all_items = Item.query.join(Tag).filter(Tag.task == task).order_by(Item.url).all()

    # make item-dicts per url
    last_url = ''
    item_dicts_per_url = []
    item_dict = {}
    for item in all_items:
        if last_url != item.url:
            last_url = item.url
            item_dict = {'url': item.url}
            item_dicts_per_url.append(item_dict)
        item_dict[item.tag] = item
    # print(item_dicts_per_url)

    # make item-lists per url for web page
    item_lists_per_url = []
    for i in range(len(item_dicts_per_url)):
        item_dict_per_url = item_dicts_per_url[i]
        items_list = [None] * len(tags)
        for j in range(len(tags)):
            items_list[j] = item_dict_per_url.get(tags[j])
        item_lists_per_url.append(items_list)
    # print(item_lists_per_url)

    return render_template('task/detail.html', task=task, tags=tags, item_lists_per_url=item_lists_per_url,
                           items_count=len(item_lists_per_url))


@task.route('/new_task', methods=['GET', 'POST'])
def new_task():
    form = NewTaskForm()
    if form.validate_on_submit():
        name = str(form.name.data)
        url = str(form.url.data)

        builder = MyCrawlSpiderBuilder(name).add_start_url(url)
        # start_my_crawl.delay(builder)
        start_my_crawl_dict.delay(builder.to_dict())

        # start_my_crawl(builder)
        # Process(target=start_my_crawl, args=(builder, )).start()

        # start_crawl.delay(name, [url])
        # start_simple_crawl.delay(name, [url])
        # start_crawl('baidu', ['http://baidu.com'])
        task = Task(name=form.name.data)
        url = Url(rule1=form.url.data)
        tag = Tag(name=form.content_name.data, rule1=form.content_rule1.data)
        task.urls.append(url)
        task.tags.append(tag)
        db.session.add(task)
        db.session.commit()
        flash('ok!')

        # start_crawl('asdf', 'http://baidu.com')
        # do_sth.delay()

        return redirect(url_for('task.new_task'))
    return render_template('task/newTask.html', form=form)
