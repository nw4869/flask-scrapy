__author__ = 'nightwind'

from flask import render_template, request
from . import main


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/ajax_test', methods=['GET', 'POST'])
def ajax_test():
    if request.method == 'POST':
        return 'param = ' + request.form['param']
    else:
        return render_template('ajax_test.html')
