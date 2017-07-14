#!/usr/bin/env python
# -*- coding:utf-8 -*-
#   
#   Author  :   XueWeiHan
#   Date    :   17/6/12 上午11:49
#   Desc    :   数据库连接、BaseModel
from peewee import Model
from playhouse.sqlite_ext import PrimaryKeyAutoIncrementField
from hellogithub import database


class BaseModel(Model):
    class Meta:
        database = database
    """
    因为 SQLite 的自增键的特殊性，所以需要
    特殊声明为 PrimaryKeyAutoIncrementField
    """
    id = PrimaryKeyAutoIncrementField()
