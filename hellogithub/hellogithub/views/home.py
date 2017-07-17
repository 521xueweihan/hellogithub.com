#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   Date    :   17/6/12 上午10:49
#   Desc    :   首页和关于页面
from urllib import quote, urlencode

import requests
from flask import render_template, session, request, redirect, abort, url_for
from playhouse.flask_utils import PaginatedQuery
from peewee import DoesNotExist

from hellogithub.models import Category, Volume, Content, User
from tools import markdown2html, make_image_url
from hellogithub import app, logger


@app.route('/')
def home():
    uuid = session.get('uuid')
    if uuid:
        try:
            user_info = User.get(User.uuid == uuid)
        except Exception:
            session.clear()
            user_info = ''
    else:
        user_info = ''
    category_objects = Category.select(Content, Category) \
        .join(Content) \
        .where(Content.status == 1) \
        .group_by(Category.id) \
        .order_by(Category.name)
    volume_objects = Volume.select().where(Volume.status == 1).order_by(
        Volume.name.desc())
    content_objects = Content.select().where(Content.status == 1)
    return render_template('home.html', user_info=user_info,
                           category_count=len(category_objects),
                           volume_count=len(volume_objects),
                           page_title=u'GitHub 上入门级、有趣、实用的开源项目',
                           project_count=len(content_objects),
                           last_volume_num=max(
                               [volume_object.name for volume_object in
                                   volume_objects]),
                           categorys=category_objects, volumes=volume_objects)


@app.route('/sign/in/')
def sign_in():
    """
    登陆通过 GitHub OAuth 实现
    参考文档：
    https://developer.github.com/apps/building-integrations/setting-up-and-reg
    istering-oauth-apps/about-authorization-options-for-oauth-apps/
    """
    code = request.args.get('code')
    if code:
        params = urlencode({
            'client_id': app.config['CLIENT_ID'],
            'client_secret': app.config['CLIENT_SECRET'],
            'code': code
        })
        try:
            access_token_response = requests.post(app.config['ACCESS_URL'],
                                                  params, timeout=10)
            github_user_response = requests.get(
                'https://api.github.com/user?' + access_token_response.text,
                timeout=10)
        except Exception as e:
            logger.error(e)
            return abort(500)
        
        github_user_json = github_user_response.json()
        github_user_id = github_user_json.get('id')
        
        name = github_user_json.get('name') or github_user_json.get('login')
        avatar_url = github_user_json.get('avatar_url')
        email = github_user_json.get('email')
        
        try:
            user_object = User.get(User.uuid == github_user_id)
            # update user info
            user_object.name = name
            user_object.avatar_url = avatar_url
            user_object.email = email
            session['is_admin'] = user_object.admin
            session['uuid'] = user_object.uuid
            return redirect(url_for('home'))
        except DoesNotExist:
            user_object = User(uuid=github_user_id, name=name,
                               avatar_url=avatar_url, email=email)
            user_object.save()
            return redirect(url_for('home'))
        except Exception as e:
            logger.error(e)
            return abort(500)
    else:
        params = urlencode({'client_id': app.config['CLIENT_ID']})
        return redirect(app.config['AUTHORIZE_URL'] + '?' + params)


@app.route('/sign/out/')
def sign_out():
    session.clear()
    return redirect(url_for('home'))


@app.route('/category/<input_category>/')
def category(input_category):
    """
    PaginatedQuery 会通过 GET 请求的 page 参数返回该页的内容
    """
    menu_url = quote(request.path.encode('utf-8'))
    content_objects = Content.select(Category, Content).join(Category) \
        .where(Category.name == input_category, Content.status == 1)
    page_object = PaginatedQuery(content_objects,
                                 paginate_by=app.config['PAGE_MAX'],
                                 check_bounds=True)
    project_objects = page_object.get_object_list()
    for project_object in project_objects:
        project_object.description = markdown2html(project_object.description)
        project_object.image_url = make_image_url(project_object.image_path)
    page_count = page_object.get_page_count()
    current_page = page_object.get_page()
    return render_template('content.html', projects=project_objects,
                           menu_url=menu_url,
                           content_type='category', page_title=input_category,
                           category_url=quote(input_category.encode('utf-8')),
                           page_count=page_count, current_page=current_page)


@app.route('/volume/<input_volume>/')
def volume(input_volume):
    menu_url = quote(request.path.encode('utf-8'))
    content_objects = Content.select(Content, Volume) \
        .join(Volume) \
        .where(Volume.name == input_volume, Volume.status == 1,
               Content.status == 1)
    category_list = Category.select().order_by(Category.name)
    
    volume_objects = Volume.select().where(Volume.status == 1).order_by(
        Volume.name.desc())
    volume_name_list = [fi_volume_obj.name for fi_volume_obj in volume_objects]
    if input_volume in volume_name_list:
        current_volume_index = volume_name_list.index(input_volume)
    else:
        current_volume_index = -1
    
    contents = []
    index_num = 0
    for category_object in category_list:
        projects = [category_object.name]  # 类别放在list第一个
        for fi_content in content_objects:
            if fi_content.category.name == category_object.name:
                index_num += 1
                title_string = u'{num}、<a target="_blank" href="{url}">' \
                               u'{title}</a>：'\
                               .format(num=index_num,
                                       title=fi_content.title,
                                       url=fi_content.project_url)\
                               + fi_content.description
                fi_content.description = markdown2html(title_string)
                fi_content.image_url = make_image_url(fi_content.image_path)
                projects.append(fi_content)
        if not len(projects) == 1:
            contents.append(projects)
    
    return render_template('content.html', contents=contents,
                           content_type='volume', menu_url=menu_url,
                           volume_name_list=volume_name_list,
                           volume_name_len=len(volume_name_list),
                           current_volume_index=current_volume_index,
                           page_title=u'第 {vol} 期'.format(vol=input_volume))


@app.route('/about/')
def about():
    content_menu_url = quote(request.args.get('url', '/').encode('utf-8'))
    return render_template('about.html', page_title=u'关于',
                           menu_url=content_menu_url)
