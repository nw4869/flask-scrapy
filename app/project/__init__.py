from flask import Blueprint

pj = Blueprint('project', __name__)

from . import views
