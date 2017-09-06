#!/usr/bin/env python
# -*- coding:utf-8 -*-
#   
#   Author  :   XueWeiHan
#   Date    :   17/8/31 下午3:02
#   Desc    :   数据库连接、BaseModel
from peewee import Model
from playhouse.db_url import connect
from playhouse.sqlite_ext import PrimaryKeyAutoIncrementField

from ..config import DATABASE_URL

database = connect(DATABASE_URL)


class BaseModel(Model):
    class Meta:
        database = database
    """
    因为 SQLite 的自增键的特殊性，所以需要
    特殊声明为 PrimaryKeyAutoIncrementField
    """
    id = PrimaryKeyAutoIncrementField()