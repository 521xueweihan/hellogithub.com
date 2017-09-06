#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   Date    :   17/3/12 上午11:23
#   Desc    :   启动入口
from hellogithub import app
from hellogithub.models.base import database
from hellogithub.models.hellogithub import Content, Category, Volume, User,\
    Collection, CollectionProject
from hellogithub.models.tiobe import TiobeRank, TiobeContent, TiobeHall


if __name__ == '__main__':
    database.create_tables(
        [Category, Volume, User, Content, Collection, CollectionProject,
         TiobeRank, TiobeContent, TiobeHall], safe=True)
    app.run(port=4000)
