#!/usr/bin/env python
# -*- coding:utf-8 -*-
#   
#   Author  :   XueWeiHan
#   Date    :   17/7/28 下午2:18
#   Desc    :   用户个人页面
from datetime import datetime

from flask import request, render_template, session, Blueprint, jsonify
from playhouse.shortcuts import model_to_dict
from peewee import IntegrityError

from . import InvalidParams, ParamsConflict, Unauthorized
from tools import models_to_dicts
from ..models import Content, User, Collection, CollectionProject, database


profile = Blueprint('profile', __name__, url_prefix='/profile')


@profile.before_request
def check_user():
    if not session.get('uuid'):
        raise Unauthorized()

    
@profile.route('/')
def user_home():
    uuid = session.get('uuid')
    user_object = User.get(User.uuid == uuid)
    return render_template('profile.html', user_info=user_object,
                           page_title=u'个人首页')


@profile.route('/collection/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def user_collection():
    uuid = session.get('uuid')
    collection_name = request.values.get('name')
    collection_id = request.values.get('collection_id')

    if request.method == 'POST':
        if not collection_name:
            raise InvalidParams()
        try:
            Collection.create(name=collection_name, uuid=uuid)
            return jsonify(
                message=u'创建收藏夹 {name} 成功'.format(name=collection_name))
        except IntegrityError:
            raise ParamsConflict
    elif request.method == 'PUT':
        if not collection_name:
            raise InvalidParams()
        update_time = datetime.now()
        Collection.update(name=collection_name, update_time=update_time)\
            .where(Collection.id == collection_id).execute()
        return jsonify(message=u'更新收藏夹 {name} 成功'.format(name=collection_name))
    elif request.method == 'DELETE':
        if not collection_id:
            raise InvalidParams()
        collection_project_objs = CollectionProject.select().join(Collection)\
            .where(Collection.id == collection_id,
                   Collection.status == 1)
        with database.transaction():
            for fi_collection_project_obj in collection_project_objs:
                CollectionProject.del_collection_project(fi_collection_project_obj.id)

            Collection.del_collection(collection_id)

        return jsonify(message=u'删除收藏夹成功')

    elif request.method == 'GET':
        collection_objs = Collection.select()\
            .where(Collection.uuid == uuid, Collection.status == 1)\
            .order_by(Collection.create_time)
        for collection_obj in collection_objs:
            collection_obj.projects = CollectionProject.select() \
                .join(Collection) \
                .where(Collection.id == collection_obj.id,
                       CollectionProject.status == 1)
        return render_template('profile_collection.html',
                               collections=collection_objs,
                               page_title=u'我的收藏')
        
        
@profile.route('/collection/project/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def collect_project():
    uuid = session.get('uuid')
    collection_id = request.values.get('collection_id')
    collect_project_id = request.values.get('project_id')
    project_name = request.values.get('project_name')
    project_url = request.values.get('project_url')

    if request.method == 'GET':
        if collect_project_id:
            # 获取单一项目信息，用于"更新"
            collect_project_obj = CollectionProject.select()\
                .where(CollectionProject.id == collect_project_id).get()
            return jsonify(payload=model_to_dict(collect_project_obj))
            
        elif collection_id:
            # 获取某一收藏夹下的所有项目
            collect_project_objs = CollectionProject.select()\
                .join(Collection)\
                .where(Collection.id == collection_id,
                       CollectionProject.status == 1)
            return jsonify(payload=models_to_dicts(collect_project_objs))
        else:
            # 获取用户所有的收藏夹
            collection_objs = Collection.select().where(
                Collection.uuid == uuid, Collection.status == 1) \
                .order_by(Collection.create_time)
            if not collection_objs:
                collection_obj = Collection.create(name=u'默认收藏夹', uuid=uuid)
                collection_objs = [collection_obj]
            return jsonify(payload=models_to_dicts(collection_objs))
        
    elif request.method == 'POST':
        if not (collection_id and project_name and project_url):
            raise InvalidParams()
        collection_obj = Collection.select()\
            .where(Collection.id == collection_id).get()
        try:
            collect_project_obj = CollectionProject.create(
                name=project_name, project_url=project_url, collection=collection_obj)
            project_obj = Content.select(Content.id).where(
                Content.project_url == project_url).get()
            
            return jsonify(message=u'收藏项目成功', payload={
                'project_id': project_obj.id,
                'collect_project_id': collect_project_obj.id})
        except IntegrityError:
            raise ParamsConflict()
    elif request.method == 'PUT':
        if not (collection_id and project_name and collect_project_id):
            raise InvalidParams()
        
        update_time = datetime.now()
        collection_obj = Collection.select()\
            .where(Collection.id == collection_id).get()

        CollectionProject\
            .update(name=project_name,
                    update_time=update_time, collection=collection_obj)\
            .where(CollectionProject.id == collect_project_id).execute()
        return jsonify(message=u'更新项目 {name} 成功'.format(name=project_name))

    elif request.method == 'DELETE':
        if not collect_project_id:
            raise InvalidParams()
        CollectionProject.del_collection_project(collect_project_id)
        return jsonify(message=u'移除收藏项目成功')
        
    
@profile.route('/subscribe/')
def subscribe():
    pass
