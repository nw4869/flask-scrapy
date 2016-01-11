from billiard import Process

__author__ = 'nightwind'

from flask import render_template, flash, redirect, url_for
from . import task
from ..models import Task, Tag
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
        db.session.add(task)
        db.session.commit()
        flash('ok!')

        # start_crawl('asdf', 'http://baidu.com')
        do_sth.delay()

        return redirect(url_for('task.new_task'))
    return render_template('task/newTask.html', form=form)
