from flask import Blueprint

task = Blueprint('task', __name__)

from . import views
