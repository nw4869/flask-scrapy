# coding: utf-8
__author__ = 'nightwind'

from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class NewTaskForm(Form):
    name = StringField(u'任务名', validators=[DataRequired(), Length(1, 255)])
    url = StringField(u'起始网址', validators=[DataRequired(), Length(1, 255)])
    rule1 = StringField(u'规则1', validators=[DataRequired(), Length(1, 255)])
    link_exclude = StringField(u'链接不得包含', validators=[Length(0, 255)])
    link_include = StringField(u'链接必须包含', validators=[Length(0, 255)])
    content_exclude = StringField(u'内容不得包含', validators=[Length(0, 255)])
    content_include = StringField(u'内容必须包含', validators=[Length(0, 255)])
    submit = SubmitField(u'提交')
