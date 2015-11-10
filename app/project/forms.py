__author__ = 'nightwind'

from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class NewProjectForm(Form):
    name = StringField('Name', validators=[DataRequired(), Length(1, 64)])
    url = StringField('Url', validators=[DataRequired(), Length(1, 64)])
    submit = SubmitField('Submit')
