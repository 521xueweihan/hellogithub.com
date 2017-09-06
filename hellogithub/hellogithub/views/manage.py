#!/usr/bin/env python
# -*- coding:utf-8 -*-
#   
#   Author  :   XueWeiHan
#   Date    :   17/6/12 上午10:49
#   Desc    :   管理后台
from datetime import datetime

from flask import render_template, request, jsonify, session, Blueprint
from peewee import DoesNotExist, IntegrityError
from playhouse.shortcuts import model_to_dict

from . import InvalidParams, ParamsConflict, Unauthorized, Forbidden
from ..models.base import database
from ..models.hellogithub import Category, Volume, Content
from tools import models_to_dicts, make_image_path, make_description, \
    get_image_name
from ..generate_markdown import generate_markdown

manage = Blueprint('manage', __name__, url_prefix='/manage')


@manage.before_request
def is_admin():
    if session.get('uuid'):
        if session.get('is_admin') is not True:
            raise Forbidden()
    else:
        raise Unauthorized()
        

@manage.route('/list/')
def project_list():
    """
    - 根据 category 条件搜索展示项目
    - 根据 volume 条件搜索展示项目
    """
    select_type = request.args.get('type', '')
    subset = request.args.get('subset', '')
    
    if select_type == 'volume' and subset:
        contents = Content.select()\
                          .join(Volume)\
                          .where(Volume.id == subset)\
                          .order_by(Content.category)
    elif select_type == 'category' and subset:
        contents = Content.select()\
                          .join(Category)\
                          .where(Category.id == subset)\
                          .order_by(Content.volume)
    else:
        raise InvalidParams()
    return jsonify(payload=models_to_dicts(contents))


@manage.route('/search/')
def search_project():
    project_url = request.args.get('project_url', '')
    if project_url:
        try:
            content = Content.select()\
                             .where(Content.project_url == project_url)\
                             .get()
            return jsonify(payload=model_to_dict(content))
        except DoesNotExist:
            return jsonify(message='未找到')
    else:
        raise InvalidParams()


@manage.route('/', methods=['GET', 'POST', 'DELETE', 'PUT'])
def manage_content():
    """
    内容管理
    """
    if request.method == 'GET':
        category_objects = Category.select().order_by(Category.name)
        volume_objects = Volume.select().order_by(Volume.name.desc())
        project_id = request.args.get('project_id')
        
        # 展示项目信息，用于更新
        if project_id:
            content_object = Content.select()\
                                    .where(Content.id == project_id)\
                                    .get()
            category_list = [
                (category_object.id, category_object.name)
                for category_object in category_objects]
            volume_list = [
                (volume_object.id, volume_object.name)
                for volume_object in volume_objects]
            result_dict = model_to_dict(content_object)
            result_dict['image_name'] = get_image_name(
                result_dict.get('image_path'))
            result_dict['category_list'] = category_list
            result_dict['volume_list'] = volume_list
            return jsonify(payload=result_dict)
        # 展示内容管理页面
        else:
            return render_template('manage/content.html', page_title=u'内容管理',
                                   categorys=category_objects,
                                   volumes=volume_objects)
    elif request.method in ['PUT', 'POST']:
        project_title = request.form.get('title')
        project_url = request.form.get('project_url')
        if not all([project_title, project_url]):
            raise InvalidParams(message=u'url 和 title 都不能为空')
        
        volume_id = request.form.get('volume_id')
        category_id = request.form.get('category_id')
        project_id = request.form.get('project_id')
        volume_object = Volume.select().where(Volume.id == volume_id)
        category_object = Category.select().where(Category.id == category_id)
        image_path = make_image_path(volume_object.get().name,
                                     request.form.get('image_name', ''))
        description = make_description(request.form.get('description', ''))
        project_data = {
            'title': project_title,
            'volume': volume_object,
            'category': category_object,
            'project_url': project_url,
            'image_path': image_path,
            'description': description,
            'update_time': datetime.now()
        }
        # 更新项目信息
        if request.method == 'PUT':
            try:
                Content.update(**project_data).where(
                    Content.id == project_id).execute()
                return jsonify(message=u'更新内容 {} 信息成功'
                               .format(project_data['title']))
            except IntegrityError:
                raise ParamsConflict(message=u'更新内容失败：{} 已存在'
                                     .format(project_url))
        # 创建项目
        else:
            try:
                Content.create(**project_data)
                return jsonify(message=u'新增内容 {} 成功'
                               .format(project_data['title']))
            except IntegrityError:
                raise ParamsConflict(message=u'新增内容失败：{} 已存在'
                                     .format(project_url))
    # 删除项目
    elif request.method == 'DELETE':
        project_id = request.form.get('project_id')
        project_title = request.form.get('project_title')
        if not all([project_id, project_title]):
            raise InvalidParams()
        
        Content.delete().where(Content.id == project_id).execute()
        return jsonify(message=u'删除内容：{} 成功'.format(project_title))


@manage.route('/category/', methods=['GET', 'POST', 'DELETE', 'PUT'])
def manage_category():
    """
    分类管理
    """
    if request.method == 'GET':
        category_id = request.args.get('category_id')
        if category_id:
            category_object = Category.select()\
                                      .where(Category.id == category_id)\
                                      .get()
            return jsonify(payload=model_to_dict(category_object))
        else:
            category_objects = Category.select().order_by(Category.id)
            return render_template('manage/category.html',
                                   categorys=category_objects,
                                   page_title=u'分类管理')
    # 新增分类
    elif request.method == 'POST':
        category_name = request.form.get('category_name', '')
        if not category_name:
            raise InvalidParams(message=u'新增分类失败：分类名不能为空')
        try:
            Category.create(name=category_name)
            return jsonify(message=u'新增分类：{}，成功'.format(category_name))
        except IntegrityError:
            raise ParamsConflict(message=u'新增分类失败：{} 已存在'
                                 .format(category_name))
    # 更新分类
    elif request.method == 'PUT':
        category_name = request.form.get('category_name')
        category_id = request.form.get('category_id')
        if not category_name:
            raise InvalidParams(message=u'更新分类失败：name 不能为空')
        
        try:
            Category.update(name=category_name,
                            update_time=datetime.now())\
                    .where(Category.id == category_id)\
                    .execute()
            return jsonify(message=u'更新分类 {} 信息成功'.format(category_name))
        except IntegrityError:
            raise ParamsConflict(message=u'更新分类失败：{} 已存在'
                                 .format(category_name))
    # 删除分类
    elif request.method == 'DELETE':
        category_id = request.form.get('category_id')
        category_name = request.form.get('category_name')
        try:
            content_query = Content.select()\
                                   .join(Category)\
                                   .where(Category.id == category_id)\
                                   .get()
            project_url = content_query.project_url
            raise InvalidParams(message=u'删除分类失败：{project_url}项目所属'
                                        u'于这个分类，请先修改该项目类别'
                                .format(project_url=project_url))
        except DoesNotExist:
            Category.delete().where(Category.id == category_id).execute()
            return jsonify(message=u'删除分类：{}，成功'.format(category_name))


@manage.route('/volume/', methods=['GET', 'POST', 'DELETE', 'PUT'])
def manage_volume():
    """
    期数管理
    """
    if request.method == 'GET':
        volume_id = request.args.get('volume_id')
        if volume_id:
            volume_object = Volume.select()\
                                  .where(Volume.id == volume_id)\
                                  .get()
            return jsonify(payload=model_to_dict(volume_object))
        else:
            volume_objects = Volume.select().order_by(Volume.name)
            return render_template('manage/volume.html',
                                   volumes=volume_objects,
                                   page_title=u'Vol.管理')
    # 新增 Vol.
    elif request.method == 'POST':
        volume_name = request.form.get('volume_name')
        if volume_name:
            try:
                Volume.create(name=volume_name)
                return jsonify(message=u'新增一期：{}，成功'.format(volume_name))
            except IntegrityError:
                raise ParamsConflict(message=u'新增一期失败：{} 已存在'
                                     .format(volume_name))
        else:
            raise InvalidParams(message=u'新增一期失败：name 不能为空')
    # 更新 Vol.
    elif request.method == 'PUT':
        volume_name = request.form.get('volume_name')
        volume_id = request.form.get('volume_id')
        if not volume_name:
            raise InvalidParams(message=u'更新 Vol. 失败：name 不能为空')
        else:
            try:
                Volume.update(name=volume_name, update_time=datetime.now())\
                      .where(Volume.id == volume_id)\
                      .execute()
                return jsonify(message=u'更新 Vol. {} 信息成功'
                               .format(volume_name))
            except IntegrityError:
                raise ParamsConflict(message=u'更新 Vol. 失败：{} 已存在'
                                     .format(volume_name))
    # 删除 Vol.
    elif request.method == 'DELETE':
        volume_id = request.form.get('volume_id')
        volume_name = request.form.get('volume_name')
        try:
            content_query = Content.select()\
                                   .join(Volume)\
                                   .where(Volume.id == volume_id)\
                                   .get()
            project_url = content_query.project_url
            raise InvalidParams(message=u'删除 Vol. 失败：{project_url}项目所属'
                                        u'于这个 Vol.，请先修改该项目期数'
                                .format(project_url=project_url))
        except DoesNotExist:
            Volume.delete().where(Volume.id == volume_id).execute()
            return jsonify(message=u'删除 Vol.：{}，成功'
                           .format(volume_name))


@manage.route('/publish/volume/', methods=['POST'])
def publish_volume():
    volume_id = request.form.get('volume_id')
    volume_object = Volume.select().where(Volume.id == volume_id).get()
    content_objects = Content.select()\
                             .join(Volume)\
                             .where(Volume.id == volume_object.id)
    # 下线
    if volume_object.status == 1:
        with database.transaction():
            for content_object in content_objects:
                content_object.status = 0
                content_object.update_time = datetime.now()
                content_object.save()
            volume_object.status = 0
            volume_object.save()
        return jsonify(message=u'{}，下线成功'.format(volume_object.name))
    # 发布
    elif volume_object.status == 0:
        with database.transaction():
            for content_object in content_objects:
                content_object.status = 1
                content_object.update_time = datetime.now()
                content_object.save()
            volume_object.status = 1
            volume_object.save()
        return jsonify(message=u'{}，发布成功'.format(volume_object.name))


@manage.route('/output/', methods=['GET'])
def output_content():
    volume_id = request.args.get('volume_id')
    output_type = request.args.get('output_type')
    markdown_output = generate_markdown(volume_id, output_type)
    return jsonify(payload=markdown_output)
