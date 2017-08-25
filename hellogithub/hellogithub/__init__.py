#!/usr/bin/env python
# -*- coding:utf-8 -*-
#   
#   Author  :   XueWeiHan
#   Date    :   17/6/9 上午9:50
import os
import traceback

from flask import Flask, request, url_for, jsonify
from playhouse.flask_utils import FlaskDB
from flask_wtf import CSRFProtect

from config import logger, flask_config
from models import database
from views import InvalidUsage
from views.home import home
from views.profile import profile
from views.manage import manage


app = Flask(__name__)
app.config.from_mapping(flask_config)
app.register_blueprint(home)
app.register_blueprint(profile)
app.register_blueprint(manage)

flask_db = FlaskDB(app, database)
CSRFProtect(app)


def dated_url_for(endpoint, **values):
    """
    重写 url_for 函数：静态文件加上时间戳，使之即时生效
    """
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

    
@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


@app.after_request
def after_request(response):
    logger.info('%s %s %s %s %s', request.method,
                request.environ.get('HTTP_X_REAL_IP', request.remote_addr),
                request.scheme, request.full_path, response.status)
    return response


@app.errorhandler(Exception)
def exceptions(e):
    tb = traceback.format_exc()
    tb = tb.decode('utf-8')
    logger.error('%s %s %s %s 5xx INTERNAL SERVER ERROR\n%s',
                 request.environ.get('HTTP_X_REAL_IP', request.remote_addr),
                 request.method, request.scheme, request.full_path, tb)
    return '500 INTERNAL SERVER ERROR', 500
