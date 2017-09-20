#!/usr/bin/env python
# -*- coding:utf-8 -*-
#   
#   Author  :   XueWeiHan
#   Date    :   17/9/15 下午4:01
#   Desc    :   GitHub 用户信息、可用代理
from datetime import datetime, date

from peewee import CharField, DateTimeField, IntegerField, DateField, \
    ForeignKeyField

from ..models.base import BaseModel


class GitHubUser(BaseModel):
    uuid = CharField(max_length=150, unique=True)
    name = CharField(max_length=150, unique=True)
    public_repos = IntegerField()
    followers = IntegerField()
    nickname = CharField(max_length=255)
    avatar_url = CharField(max_length=255)
    html_url = CharField(max_length=255)
    location = CharField(max_length=255)
    email = CharField(max_length=255, null=True)
    fetch_date = DateField(default=date.today)
    create_time = DateTimeField(default=datetime.now)
    update_time = DateTimeField(default=datetime.now)


class GitHubData(BaseModel):
    name = CharField(max_length=150)
    stars_count = IntegerField(default=0)
    language = CharField(max_length=255, null=True)
    fetch_date = DateField(default=date.today)
    create_time = DateTimeField(default=datetime.now)

    class Meta:
        indexes = (
            # create a unique on name/fetch_date
            (('name', 'fetch_date'), True),)


class Proxy(BaseModel):
    url = CharField(max_length=150, unique=True)
    status = IntegerField(default=1)
    create_time = DateTimeField(default=datetime.now)
    update_time = DateTimeField(default=datetime.now)
    reset_time = DateTimeField(null=True, default=None)