# -*- coding: utf-8 -*-

from flask import Blueprint

blueprint = Blueprint('base', __name__)

@blueprint.route('/')
def index():
    return 'chiwanbot'
