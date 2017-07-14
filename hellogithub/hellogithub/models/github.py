#!/usr/bin/env python
# -*- coding:utf-8 -*-
#   
#   Author  :   XueWeiHan
#   Date    :   17/6/9 上午10:02
#   Desc    :   Models
from datetime import datetime

from peewee import CharField, TextField, DateTimeField, IntegerField, \
    ForeignKeyField

from base import BaseModel


class Category(BaseModel):
    name = CharField(unique=True)
    create_time = DateTimeField(default=datetime.now)
    update_time = DateTimeField(default=datetime.now)


class Volume(BaseModel):
    name = CharField(unique=True)
    create_time = DateTimeField(default=datetime.now)
    update_time = DateTimeField(default=datetime.now)
    status = IntegerField(default=0)


class Content(BaseModel):
    project_url = CharField(unique=True)
    title = CharField()
    description = TextField()
    image_path = TextField(null=True)
    category = ForeignKeyField(Category)
    volume = ForeignKeyField(Volume)
    create_time = DateTimeField(default=datetime.now)
    update_time = DateTimeField(default=datetime.now)
    status = IntegerField(default=0)


class User(BaseModel):
    name = CharField()
    uuid = IntegerField(unique=True)
    admin = IntegerField(default=0)
    avatar_url = CharField(null=True)
    email = CharField(null=True)
    status = IntegerField(default=0)

