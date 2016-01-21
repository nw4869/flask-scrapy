# coding=utf-8
from billiard import Process

__author__ = 'nightwind'

from flask import render_template, flash, redirect, url_for, abort
from . import task
from ..models import Task, Tag, Url, Item
from .forms import NewTaskForm, NewTagForm
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
        item = Item.query.join(Tag).filter(Tag.task_id == task_id, Item.id == item_id).one()
        return item.data
    except:
        pass
    abort(404)


@task.route('/id/<task_id>/start')
def start(task_id):
    try:
        task = db.session.query(Task).filter(Task.id == task_id).one()
    except:
        abort(404)

    builder = MyCrawlSpiderBuilder(task.name)
    for url in task.urls:
        if url.type == 0:
            builder.add_start_url(url.rule1)
        elif url.type == 1:
            builder.add_link_rule(url.rule1)
    for tag in task.tags:
        builder.add_tags(tag.id, tag.rule1)
    start_my_crawl_dict.delay(builder.to_dict())
    flash(u'任务启动成功!')
    return redirect(url_for('task.index'))


@task.route('/id/<task_id>')
def detail(task_id):
    try:
        task = db.session.query(Task).filter(Task.id == task_id).one()
    except:
        abort(404)
    tags = Tag.query.filter(Tag.task == task).all()

    start_urls = Url.query.filter(Url.task == task, Url.type == 0).all()

    link_rules = Url.query.filter(Url.task == task, Url.type != 0).all()

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
    urls = []
    for i in range(len(item_dicts_per_url)):
        item_dict_per_url = item_dicts_per_url[i]
        items_list = [None] * len(tags)
        for j in range(len(tags)):
            items_list[j] = item_dict_per_url.get(tags[j])
        urls.append(item_dict_per_url.get('url'))
        item_lists_per_url.append(items_list)
    # print(item_lists_per_url)

    return render_template('task/detail.html', task=task, tags=tags, item_lists_per_url=item_lists_per_url, urls=urls,
                           start_urls=start_urls, link_rules=link_rules)


@task.route('/id/<task_id>/new_tag', methods=['GET', 'POST'])
def new_tag(task_id):
    if Task.query.filter(Task.id == task_id).count() != 1:
        abort(404)

    form = NewTagForm()
    if form.validate_on_submit():
        tag = Tag(name=form.name.data, rule1=form.rule1.data, task_id=task_id)
        db.session.add(tag)
        db.session.commit()
        flash(u'添加成功!')
        return redirect(url_for('task.detail', task_id=task_id))
    return render_template('task/newTag.html', form=form)


@task.route('/id/<task_id>/remove_tag/<tag_id>', methods=['GET', 'POST'])
def remove_tag(task_id, tag_id):
    try:
        tag = Tag.query.filter(Task.id == task_id).filter(Tag.id == tag_id).one()
        db.session.delete(tag)
        db.session.commit()
        flash(u'删除成功')
        return redirect(url_for('task.detail', task_id=task_id))
    except:
        abort(404)


@task.route('/new_task', methods=['GET', 'POST'])
def new_task():
    form = NewTaskForm()
    if form.validate_on_submit():
        name = form.name.data  # .encode('utf-8')
        url = form.url.data  # .encode('utf-8')

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
        url_rule = Url(rule1=form.link_rule.data, type=1)
        task.urls.append(url)
        task.urls.append(url_rule)
        db.session.add(task)
        db.session.commit()
        flash(u'添加成功!')

        # start_crawl('asdf', 'http://baidu.com')
        # do_sth.delay()

        # return redirect(url_for('task.new_task'))
        return redirect(url_for('task.detail', task_id=task.id))
    return render_template('task/newTask.html', form=form)
