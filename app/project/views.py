__author__ = 'nightwind'

from flask import render_template, flash, redirect, url_for
from . import pj
from ..models import Project, Item
from .forms import NewProjectForm
from ..tasks import do_sth, start_crawl
from .. import db
from time import sleep


@pj.route('/')
def index():
    # start_crawl.delay('baidu', ['http://baidu.com'])
    task = do_sth.delay()
    sleep(0.1)
    print(task.ready())

    print(task.status)

    projects = Project.query.all()
    return render_template("project/index.html", projects=projects)


@pj.route('/new_project', methods=['GET', 'POST'])
def new_project():
    form = NewProjectForm()
    if form.validate_on_submit():
        name = str(form.name.data)
        url = str(form.url.data)
        start_crawl.delay(name, [url])
        # start_simple_crawl.delay(name, [url])
        # start_crawl('baidu', ['http://baidu.com'])
        project = Project(name=form.name.data)
        db.session.add(project)
        db.session.commit()
        flash('ok!')

        # start_crawl('asdf', 'http://baidu.com')
        do_sth()

        return redirect(url_for('project.new_project'))
    return render_template('project/newProject.html', form=form)
