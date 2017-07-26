#!/usr/bin/env python
# -*- coding:utf-8 -*-
#   
#   Author  :   XueWeiHan
#   Date    :   17/6/12 上午10:49
#   Desc    :   管理后台
import functools
from datetime import datetime

from flask import render_template, request, jsonify, session, abort
from peewee import DoesNotExist, IntegrityError
from playhouse.shortcuts import model_to_dict

from hellogithub.models import Category, Volume, Content
from tools import models_to_dicts, make_image_path, make_description, \
    get_image_name
from hellogithub.generate_markdown import generate_markdown
from hellogithub import app, logger, database


def login(f):
    @functools.wraps(f)
    def warp_fun(*args, **kwargs):
        if session.get('is_admin') == 1:
            return f(*args, **kwargs)
        else:
            logger.warning('Guest request fail.')
            abort(404)
    
    return warp_fun


@app.route('/manage/list/')
@login
def project_list():
    """
    - 根据 category 条件搜索展示项目
    - 根据 volume 条件搜索展示项目
    """
    select_type = request.args.get('type', '')
    subset = request.args.get('subset', '')
    
    if select_type == 'volume' and subset:
        content_objects = Content.select() \
            .join(Volume) \
            .where(Volume.id == subset) \
            .order_by(Content.category.name)
        content_dicts = models_to_dicts(content_objects)
    elif select_type == 'category' and subset:
        content_objects = Content.select() \
            .join(Category) \
            .where(Category.id == subset) \
            .order_by(Content.volume.name)
        content_dicts = models_to_dicts(content_objects)
    else:
        content_dicts = []
        return jsonify(code=400, message=content_dicts)
    return jsonify(code=200, message=content_dicts)


@app.route('/manage/search/')
@login
def search_project():
    project_url = request.args.get('project_url', '')
    if project_url:
        try:
            content_object = Content.select().where(
                Content.project_url == project_url).get()
        except DoesNotExist:
            return jsonify(code=400, message={})
        content_dict = model_to_dict(content_object)
        return jsonify(code=200, message=content_dict)
    else:
        return jsonify(code=400, message={})


@app.route('/manage/', methods=['GET', 'POST', 'DELETE', 'PUT'])
@login
def manage_content():
    """
    内容管理
    """
    if request.method == 'GET':
        category_objects = Category.select().order_by(Category.name)
        volume_objects = Volume.select().order_by(Volume.name.desc())
        
        project_id = request.args.get('project_id')
        if project_id:
            # 展示项目信息，用于更新
            content_object = Content.select().where(
                Content.id == project_id).get()
            result_dict = model_to_dict(content_object)
            result_dict['image_name'] = get_image_name(
                result_dict.get('image_path'))
            category_list = [
                (category_object.id, category_object.name)
                for category_object in category_objects]
            volume_list = [
                (volume_object.id, volume_object.name)
                for volume_object in volume_objects]
            result_dict['category_list'] = category_list
            result_dict['volume_list'] = volume_list
            return jsonify(code=200, message=result_dict)
        else:
            # 动态生成 内容管理 页面
            return render_template('manage_content.html',
                                   categorys=category_objects,
                                   volumes=volume_objects,
                                   page_title=u'内容管理')
    elif request.method in ['PUT', 'POST']:
        project_title = request.form.get('title')
        project_url = request.form.get('project_url')
        if not all([project_title, project_url]):
            return jsonify(code=400,
                           message=u'project_url 和 project_title 都不能为空')
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
                return jsonify(code=200,
                               message=u'更新内容 {title} 信息成功'.format(
                                   title=project_data['title']))
            except IntegrityError:
                return jsonify(code=400,
                               message=u'更新内容失败：{project_url} 已存在'.format(
                                   project_url=project_url))
        # 创建项目
        else:
            try:
                Content.create(**project_data)
                return jsonify(code=200,
                               message=u'新增内容 {title} 成功'.format(
                                   title=project_data['title']))
            except IntegrityError:
                return jsonify(code=400,
                               message=u'新增内容失败：{project_url} 已存在'.format(
                                   project_url=project_url))
    elif request.method == 'DELETE':
        # 删除项目
        project_id = request.form.get('project_id')
        project_title = request.form.get('project_title')
        if not all([project_id, project_title]):
            return jsonify(code=400,
                           message=u'删除内容失败：project_id 和 project_title 都不能为空')
        Content.delete().where(Content.id == project_id).execute()
        return jsonify(code=200,
                       message=u'删除内容：{title}，成功'.format(title=project_title))


@app.route('/manage/category/', methods=['GET', 'POST', 'DELETE', 'PUT'])
@login
def manage_category():
    """
    分类管理
    """
    if request.method == 'GET':
        category_id = request.args.get('category_id')
        if category_id:
            category_object = Category.select().where(
                Category.id == category_id).get()
            result_dict = model_to_dict(category_object)
            return jsonify(code=200, message=result_dict)
        else:
            category_objects = Category.select().order_by(Category.id)
            return render_template('manage_category.html',
                                   categorys=category_objects,
                                   page_title=u'分类管理')
    elif request.method == 'POST':
        # 新增分类
        category_name = request.form.get('category_name', '')
        if category_name:
            try:
                Category.create(name=category_name)
                return jsonify(code=200,
                               message=u'新增分类：{name}，成功'.format(
                                   name=category_name))
            except IntegrityError:
                return jsonify(code=400,
                               message=u'新增分类失败：{category_name} 已存在'.format(
                                   category_name=category_name))
        else:
            return jsonify(code=400, message=u'新增分类失败：分类名不能为空')
    elif request.method == 'PUT':
        # 更新分类
        category_name = request.form.get('category_name')
        category_id = request.form.get('category_id')
        if not category_name:
            return jsonify(code=400,
                           message=u'更新分类失败：category_name 不能为空')
        else:
            try:
                Category.update(name=category_name,
                                update_time=datetime.now()) \
                    .where(Category.id == category_id).execute()
                return jsonify(code=200,
                               message=u'更新分类 {name} 信息成功'.format(
                                   name=category_name))
            except IntegrityError:
                return jsonify(code=400,
                               message=u'更新分类失败：{name} 已存在'.format(
                                   name=category_name))
    elif request.method == 'DELETE':
        # 删除分类
        category_id = request.form.get('category_id')
        category_name = request.form.get('category_name')
        try:
            content_query = Content.select() \
                .join(Category) \
                .where(Category.id == category_id).get()
            project_url = content_query.project_url
            return jsonify(code=400, message=u'删除分类失败：{project_url}项目所属'
                                             u'于这个分类，请先修改该项目类别'
                           .format(project_url=project_url))
        except DoesNotExist:
            Category.delete().where(Category.id == category_id).execute()
            return jsonify(code=200, message=u'删除分类：{name}，成功'
                           .format(name=category_name))


@app.route('/manage/volume/', methods=['GET', 'POST', 'DELETE', 'PUT'])
@login
def manage_volume():
    """
    期数管理
    """
    if request.method == 'GET':
        volume_id = request.args.get('volume_id')
        if volume_id:
            volume_object = Volume.select().where(Volume.id == volume_id).get()
            result_dict = model_to_dict(volume_object)
            return jsonify(code=200, message=result_dict)
        else:
            volume_objects = Volume.select().order_by(Volume.name)
            return render_template('manage_volume.html',
                                   volumes=volume_objects,
                                   page_title=u'Vol.管理')
    elif request.method == 'POST':
        # 新增一期
        volume_name = request.form.get('volume_name')
        if volume_name:
            try:
                Volume.create(name=volume_name)
                return jsonify(code=200,
                               message=u'新增一期：{name}，成功'.format(
                                   name=volume_name))
            except IntegrityError:
                return jsonify(code=400,
                               message=u'新增一期失败：{name} 已存在'.format(
                                   name=volume_name))
        else:
            return jsonify(code=400, message=u'新增一期失败：volume_name 不能为空')
    elif request.method == 'PUT':
        # 更新 Vol.
        volume_name = request.form.get('volume_name')
        volume_id = request.form.get('volume_id')
        if not volume_name:
            return jsonify(code=400,
                           message=u'更新 Vol. 失败：volume_name 不能为空')
        else:
            try:
                Volume.update(name=volume_name, update_time=datetime.now()) \
                    .where(Volume.id == volume_id).execute()
                return jsonify(code=200,
                               message=u'更新 Vol. {name} 信息成功'.format(
                                   name=volume_name))
            except IntegrityError:
                return jsonify(code=400,
                               message=u'更新 Vol. 失败：{name} 已存在'.format(
                                   name=volume_name))
    elif request.method == 'DELETE':
        # 删除 Vol.
        volume_id = request.form.get('volume_id')
        volume_name = request.form.get('volume_name')
        try:
            content_query = Content.select() \
                .join(Volume) \
                .where(Volume.id == volume_id).get()
            project_url = content_query.project_url
            return jsonify(code=400, message=u'删除 Vol. 失败：{project_url}项目所属'
                                             u'于这个 Vol.，请先修改该项目期数'
                           .format(project_url=project_url))
        except DoesNotExist:
            Volume.delete().where(Volume.id == volume_id).execute()
            return jsonify(code=200, message=u'删除 Vol.：{name}，成功'
                           .format(name=volume_name))


@app.route('/manage/publish/volume/', methods=['POST'])
@login
def publish_volume():
    volume_id = request.form.get('volume_id')
    volume_object = Volume.select().where(Volume.id == volume_id).get()
    content_objects = Content.select().join(Volume).where(
        Volume.id == volume_object.id)
    
    if volume_object.status == 1:
        with database.transaction():
            for content_object in content_objects:
                content_object.status = 0
                content_object.update_time = datetime.now()
                content_object.save()
            volume_object.status = 0
            volume_object.save()
        return jsonify(code=200,
                       message=u'{name}，下线成功'.format(name=volume_object.name))
    elif volume_object.status == 0:
        with database.transaction():
            for content_object in content_objects:
                content_object.status = 1
                content_object.update_time = datetime.now()
                content_object.save()
            volume_object.status = 1
            volume_object.save()
        return jsonify(code=200,
                       message=u'{name}，发布成功'.format(name=volume_object.name))


@app.route('/manage/output/', methods=['GET'])
@login
def output_content():
    volume_id = request.args.get('volume_id')
    output_type = request.args.get('output_type')
    markdown_output = generate_markdown(volume_id, output_type)
    return jsonify(code=200, message=markdown_output)
