__author__ = 'nightwind'

from . import db


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    status = db.Column(db.Integer, default=0, nullable=True)
    headers = db.Column(db.String, nullable=True)
    proxy = db.Column(db.String, nullable=True)
    thread_num = db.Column(db.Integer, default=1)
    delay_ms = db.Column(db.Integer, default=-1)
    urls = db.relationship('Url', backref='url', lazy='dynamic')
    tags = db.relationship('Tag', backref='tag', lazy='dynamic')


class Url(db.Model):
    __tablename__ = 'urls'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=0)
    rule1 = db.Column(db.String)
    rule2 = db.Column(db.String, nullable=True)
    exclude = db.Column(db.String, nullable=True)
    include = db.Column(db.String, nullable=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))
    # task = db.relationship(Task, 'urls', backref=db.backref('task', useList=True), lazy='dynamic')


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    rule1 = db.Column(db.String)
    rule2 = db.Column(db.String, nullable=True)
    exclude = db.Column(db.String, nullable=True)
    include = db.Column(db.String, nullable=True)
    type = db.Column(db.Integer, default=0)
    items = db.relationship('Item', backref='item', lazy='dynamic')
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String, nullable=True)
    url = db.Column(db.String)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'))
