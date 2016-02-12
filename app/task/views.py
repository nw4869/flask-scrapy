# coding=utf-8
from sqlalchemy import desc

__author__ = 'nightwind'

from flask import render_template, flash, redirect, url_for, abort, request, jsonify
from . import task
from ..models import Task, Tag, Url, Item, Result
from .forms import NewTaskForm, NewTagForm
from ..tasks import do_sth, start_crawl, start_my_crawl, start_my_crawl_dict
from .. import db
from time import sleep
from ..crawler import MyCrawlSpider, MyCrawlSpiderBuilder


@task.route('/')
def index():
    # start_crawl.delay('baidu', ['http://baidu.com'])
    task = do_sth.delay()
    # sleep(0.1)
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

    builder = MyCrawlSpiderBuilder(task.name, task_id)
    for url in task.urls:
        if url.type == 0:
            builder.add_start_url(url.rule1)
        elif url.type == 1:
            builder.add_link_rule(url.rule1)
    for tag in task.tags:
        builder.add_tags(tag.id, tag.rule1)
    start_my_crawl_dict.delay(builder.to_dict())
    flash(u'任务启动成功!')
    return redirect(request.referrer or url_for('task.index'))


@task.route('/id/<task_id>')
def detail(task_id):
    try:
        task = db.session.query(Task).filter(Task.id == task_id).one()
    except:
        abort(404)
    tags = Tag.query.filter(Tag.task == task).all()

    start_urls = Url.query.filter(Url.task == task, Url.type == 0).all()

    link_rules = Url.query.filter(Url.task == task, Url.type != 0).all()

    # results = Result.query.filter(Result.task == task).order_by(Result.datetime).all()

    return render_template('task/detail.html', task=task, tags=tags,
                           # results=results,
                           start_urls=start_urls, link_rules=link_rules, new_tag_form=NewTagForm())


@task.route('/id/<task_id>/new_tag', methods=['POST'])
def new_tag(task_id):
    if Task.query.filter(Task.id == task_id).count() != 1:
        abort(404)

    form = NewTagForm()
    if form.validate_on_submit():
        tag = Tag(name=form.name.data, rule1=form.rule1.data, task_id=task_id, type=form.type.data)
        db.session.add(tag)
        db.session.commit()
        # TODO 完善 jsonify
        return jsonify(tag={
            'id': tag.id,
            'name': tag.name,
            'type': tag.type,
            'rule1': tag.rule1,
            'task_id': task_id
        })
    return jsonify(tag=None)


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
        # name = form.name.data  # .encode('utf-8')
        # url = form.url.data  # .encode('utf-8')

        # builder = MyCrawlSpiderBuilder(name).add_start_url(url)
        # start_my_crawl.delay(builder)
        # start_my_crawl_dict.delay(builder.to_dict())

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


@task.route('/id/<int:task_id>/status', methods=['GET'])
def status(task_id):
    return jsonify(status='completed')


@task.route('/id/<task_id>/results')
def results(task_id):
    # return ''
    results = Result.query.filter(Result.task_id == task_id).order_by(desc(Result.datetime)).all()
    tags = Tag.query.filter(Tag.task_id == task_id).all()
    result_list = []
    tag_list = []
    for result in results:
        rst = {
            'id': result.id,
            'url': result.url,
            'datetime': result.datetime,
            'items': []
        }
        result_list.append(rst)
        for item in result.items:
            rst['items'].append({
                'id': item.id,
                'data': item.data,
                'tag_id': item.tag_id,
            })
    for tag in tags:
        tag_list.append({
            'id': tag.id,
            'name': tag.name
        })
    return jsonify(results=result_list, tags = tag_list)