__author__ = 'nightwind'

from . import db


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    status = db.Column(db.Integer, default=0, nullable=True)
    urls = db.relationship('Url', backref='url', lazy='dynamic')
    items = db.relationship('Item', backref='item', lazy='dynamic')


class Url(db.Model):
    __tablename__ = 'urls'
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    rule = db.Column(db.String)
    type = db.Column(db.Integer)
    datas = db.relationship('Data', backref='data', lazy='dynamic')
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))


class Data(db.Model):
    __tablename__ = 'datas'
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String, nullable=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
