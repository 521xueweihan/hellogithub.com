#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   db.Date    :   2022-05-17 11:03
#   Desc    :
from flask_sqlalchemy import SQLAlchemy

from flask import Flask

from config import Config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from website.home import home
    app.register_blueprint(home)

    return app
