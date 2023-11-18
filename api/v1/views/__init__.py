#!/usr/bin/python3
"""blueprint"""
from flask import Blueprint
from api.views.index import *

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
