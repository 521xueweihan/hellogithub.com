#!/usr/bin/env python
# -*- coding:utf-8 -*-
#   
#   Author  :   XueWeiHan
#   Date    :   17/6/9 上午10:02
#   Desc    :   Models
from datetime import datetime

from peewee import CharField, TextField, DateTimeField, IntegerField, \
    ForeignKeyField, IntegrityError

from ..models.base import BaseModel


class Category(BaseModel):
    name = CharField(max_length=150, unique=True)
    create_time = DateTimeField(default=datetime.now)
    update_time = DateTimeField(default=datetime.now)


class Volume(BaseModel):
    name = CharField(max_length=150, unique=True)
    create_time = DateTimeField(default=datetime.now)
    update_time = DateTimeField(default=datetime.now)
    status = IntegerField(default=0)


class Content(BaseModel):
    project_url = CharField(max_length=150, unique=True)
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
    status = IntegerField(default=1)


class Collection(BaseModel):
    name = CharField(max_length=150)
    uuid = IntegerField()
    status = IntegerField(default=1)
    create_time = DateTimeField(default=datetime.now)
    update_time = DateTimeField(default=datetime.now)

    class Meta:
        indexes = (
            # create a unique on uuid/name/status
            (('uuid', 'name', 'status'), True),)
    
    @staticmethod
    def del_collection(collection_id):
        try:
            Collection \
                .update(status=0, update_time=datetime.now()) \
                .where(Collection.id == collection_id).execute()
        except IntegrityError:
            collection_obj = Collection.select()\
                .where(Collection.id == collection_id).get()
            collection_obj.name += datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            collection_obj.status = 0
            collection_obj.update_time = datetime.now()
            collection_obj.save()


class CollectionProject(BaseModel):
    name = CharField()
    project_url = CharField(max_length=150)
    collection = ForeignKeyField(Collection)
    status = IntegerField(default=1)
    create_time = DateTimeField(default=datetime.now)
    update_time = DateTimeField(default=datetime.now)
    
    class Meta:
        indexes = (
            # create a unique on project_url/collection/status
            (('project_url', 'collection', 'status'), True),)
    
    @staticmethod
    def del_collection_project(collection_project_id):
        try:
            CollectionProject \
                .update(status=0, update_time=datetime.now()) \
                .where(CollectionProject.id == collection_project_id).execute()
        except IntegrityError:
            collection_project_obj = CollectionProject.select() \
                .where(CollectionProject.id == collection_project_id).get()
            # 删除 status 为 0 的记录
            CollectionProject.delete() \
                .where(
                CollectionProject.collection == collection_project_obj.collection.id,
                CollectionProject.project_url == collection_project_obj.project_url,
                CollectionProject.status == 0) \
                .execute()
        
            collection_project_obj.status = 0
            collection_project_obj.update_time = datetime.now()
            collection_project_obj.save()
