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
from ..models.base import database
from ..models.hellogithub import Content, User, Collection, CollectionProject
from tools import models_to_dicts


profile = Blueprint('profile', __name__, url_prefix='/profile')


@profile.before_request
def check_user():
    if not session.get('uuid'):
        raise Unauthorized()

    
@profile.route('/')
def user_home():
    uuid = session.get('uuid')
    user_object = User.get(User.uuid == uuid)
    return render_template('profile/home.html', user_info=user_object,
                           page_title=u'个人首页')


@profile.route('/collection/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def user_collection():
    uuid = session.get('uuid')
    collection_name = request.values.get('name')
    collection_id = request.values.get('collection_id')

    if request.method == 'GET':
        collections = Collection.select()\
                                .where(Collection.uuid == uuid,
                                       Collection.status == 1)\
                                .order_by(Collection.create_time)
        for fi_collection in collections:
            fi_collection.projects = CollectionProject.select() \
                                                      .join(Collection) \
                                                      .where(Collection.id ==
                                                             fi_collection.id,
                                                             CollectionProject.status == 1)
        return render_template('profile/collection.html',
                               collections=collections,
                               page_title=u'我的收藏')
    # 创建收藏夹
    elif request.method == 'POST':
        if not collection_name:
            raise InvalidParams()
        try:
            Collection.create(name=collection_name, uuid=uuid)
            return jsonify(message=u'创建收藏夹 {} 成功'
                           .format(collection_name))
        except IntegrityError:
            raise ParamsConflict()
        
    # 更新收藏夹
    elif request.method == 'PUT':
        if not collection_name:
            raise InvalidParams()
        
        update_time = datetime.now()
        Collection.update(name=collection_name, update_time=update_time)\
            .where(Collection.id == collection_id).execute()
        return jsonify(message=u'更新收藏夹 {} 成功'.format(collection_name))
    
    # 删除收藏夹
    elif request.method == 'DELETE':
        if not collection_id:
            raise InvalidParams()
        
        collection_projects = CollectionProject.select()\
                                               .join(Collection)\
                                               .where(Collection.id == collection_id,
                                                      Collection.status == 1)
        with database.transaction():
            for fi_collection_project in collection_projects:
                CollectionProject.del_collection_project(fi_collection_project.id)

            Collection.del_collection(collection_id)
        return jsonify(message=u'删除收藏夹成功')


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
            collect_projects = CollectionProject.select()\
                .join(Collection).where(Collection.id == collection_id,
                                        CollectionProject.status == 1)
            return jsonify(payload=models_to_dicts(collect_projects))
        else:
            # 获取用户所有的收藏夹
            collections = Collection.select()\
                                    .where(Collection.uuid == uuid,
                                           Collection.status == 1) \
                                    .order_by(Collection.create_time)
            # 初始化'默认收藏夹'
            if not collections:
                collection = Collection.create(name=u'默认收藏夹', uuid=uuid)
                collections = [collection]
            return jsonify(payload=models_to_dicts(collections))
    # 新增收藏项目
    elif request.method == 'POST':
        if not (collection_id and project_name and project_url):
            raise InvalidParams()
        
        collection = Collection.select()\
                               .where(Collection.id == collection_id)\
                               .get()
        try:
            collection_project = CollectionProject.create(name=project_name,
                                                          project_url=project_url,
                                                          collection=collection)
            project = Content.select(Content.id)\
                             .where(Content.project_url == project_url)\
                             .get()
            
            return jsonify(message=u'收藏项目成功',
                           payload={'project_id': project.id,
                                    'collect_project_id': collection_project.id})
        except IntegrityError:
            raise ParamsConflict()
    # 更新收藏项目的信息
    elif request.method == 'PUT':
        if not (collection_id and project_name and collect_project_id):
            raise InvalidParams()
        
        update_time = datetime.now()
        collection = Collection.select()\
                               .where(Collection.id == collection_id)\
                               .get()
        CollectionProject.update(name=project_name,
                                 update_time=update_time,
                                 collection=collection)\
                         .where(CollectionProject.id == collect_project_id)\
                         .execute()
        return jsonify(message=u'更新项目 {} 成功'.format(project_name))
    # 取消收藏
    elif request.method == 'DELETE':
        if not collect_project_id:
            raise InvalidParams()
        
        CollectionProject.del_collection_project(collect_project_id)
        return jsonify(message=u'移除收藏项目成功')
        
    
@profile.route('/subscribe/')
def subscribe():
    pass
