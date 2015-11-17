__author__ = 'nightwind'

from . import db


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    status = db.Column(db.Integer, default=0, nullable=True)
    urls = db.relationship('Url', backref='url', lazy='dynamic')
    tags = db.relationship('Tag', backref='tag', lazy='dynamic')


class Url(db.Model):
    __tablename__ = 'urls'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer)
    data = db.Column(db.String)
    project_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    rule1 = db.Column(db.String)
    rule2 = db.Column(db.String, nullable=True)
    rule3 = db.Column(db.String, nullable=True)
    type = db.Column(db.Integer)
    items = db.relationship('Item', backref='item', lazy='dynamic')
    project_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String, nullable=True)
    item_id = db.Column(db.Integer, db.ForeignKey('tags.id'))
