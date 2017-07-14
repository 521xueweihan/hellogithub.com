#!/usr/bin/env python
# -*- coding:utf-8 -*-
#   
#   Author  :   XueWeiHan
#   Date    :   17/6/9 上午9:50
import os
import logging
from logging.handlers import RotatingFileHandler
import traceback

from flask import Flask, request, url_for
from playhouse.flask_utils import FlaskDB

import config

app = Flask(__name__)
app.config.from_object(config)

flask_db = FlaskDB(app)
database = flask_db.database


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

handler = RotatingFileHandler('%s.log' % app.name, maxBytes=10000000, backupCount=3)
logger = logging.getLogger(app.name)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

from views import *