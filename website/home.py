#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   db.Date    :   2022-05-07 19:20
#   Desc    :
from flask import render_template, Blueprint
from website.curd.home import get_repos

home = Blueprint('home', __name__)

@home.route('/')
def hello_world():  # put application's code here
    repos, has_more = get_repos()
    return render_template('index.html', repos=repos)
