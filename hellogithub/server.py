#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   Date    :   17/3/12 上午11:23
#   Desc    :   启动入口
from hellogithub import app, database
from hellogithub.models import Content, Category, Volume, User


if __name__ == '__main__':
    database.create_tables([Category, Volume, Content, User], safe=True)
    app.run(port=4000)
