#!/usr/bin/env python
# -*- coding:utf-8 -*-
#   
#   Author  :   XueWeiHan
#   Date    :   17/8/30 下午5:33
#   Desc    :   Model
from datetime import datetime, date

from peewee import CharField, TextField, DateTimeField, IntegerField, DateField

from ..models.base import BaseModel


class TiobeRank(BaseModel):
    language = CharField(max_length=150)
    position = IntegerField()
    rating = CharField(max_length=150)
    rating_int = IntegerField()
    publish_date = DateField(default=date.today)
    create_time = DateTimeField(default=datetime.now)


class TiobeContent(BaseModel):
    title = CharField(max_length=255)
    description = TextField()
    translation_desc = TextField(null=True)
    translation_title = CharField(null=True)
    chart_str = TextField()
    publish_date = DateField(default=date.today)
    create_time = DateTimeField(default=datetime.now)


class TiobeHall(BaseModel):
    year = IntegerField()
    language = CharField()
    publish_date = DateField(default=date.today)
    create_time = DateTimeField(default=datetime.now)
