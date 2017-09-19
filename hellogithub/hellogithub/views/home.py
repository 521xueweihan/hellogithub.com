#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   Date    :   17/6/12 上午10:49
#   Desc    :   首页和关于页面
import random
from urllib import quote, urlencode

import requests
from flask import render_template, session, request, redirect, abort, url_for, \
    Blueprint
from playhouse.flask_utils import PaginatedQuery
from peewee import DoesNotExist

from tools import markdown2html, make_image_url
from ..models.hellogithub import Category, Volume, Content, User, Collection, \
    CollectionProject
from ..models.tiobe import TiobeContent, TiobeHall, TiobeRank
from ..config import CLIENT_ID, CLIENT_SECRET, ACCESS_URL, PAGE_MAX, \
    AUTHORIZE_URL, logger

home = Blueprint('home', __name__)


def update_session(user_object):
    # update session
    session['is_login'] = True
    session['uuid'] = user_object.uuid
    if user_object.admin:
        session['is_admin'] = True
    else:
        session['is_admin'] = False


def get_collected_project_status(project_url):
    uuid = session.get('uuid')
    # 找到已登录的用户收藏的项目
    if uuid:
        collected_projects = CollectionProject.select(CollectionProject,
                                                      Collection)\
                                              .join(Collection) \
                                              .where(CollectionProject.status == 1,
                                                     Collection.uuid == uuid)
        collected_project_list = [
            {fi_collected_project_obj.project_url: fi_collected_project_obj.id}
            for fi_collected_project_obj in collected_projects]
    else:
        collected_project_list = []

    for fi_collected_project in collected_project_list:
        if fi_collected_project.get(project_url):
            return 1, fi_collected_project.get(project_url)
    return 0, 0


def get_user_collections_list():
    uuid = session.get('uuid')
    if uuid:
        collections = Collection.select()\
                                .where(Collection.uuid == uuid,
                                       Collection.status == 1)\
                                .order_by(Collection.create_time)
        if not collections:
            collection = Collection.create(name=u'默认收藏夹', uuid=uuid)
            collections = [collection]
    else:
        return []
    return collections


@home.route('/')
def index():
    uuid = session.get('uuid')
    user_info = ''

    try:
        user_info = User.get(User.uuid == uuid)
    except DoesNotExist:
        session.clear()

    categories = Category.select(Content, Category) \
                         .join(Content) \
                         .where(Content.status == 1) \
                         .group_by(Category.id) \
                         .order_by(Category.name)
    
    # category_name urlencode
    for fi_category in categories:
        fi_category.quote_name = quote(fi_category.name.encode('utf-8'))
        
    volumes = Volume.select(Volume.name)\
                    .where(Volume.status == 1)\
                    .order_by(Volume.name.desc())
    contents = Content.select().where(Content.status == 1)
    select_category = random.choice(categories)
    
    return render_template('home/home.html', user_info=user_info,
                           page_title=u'分享 GitHub 上入门级、有趣的开源项目',
                           contents=contents,
                           select_category=select_category,
                           categories=categories, volumes=volumes)


@home.route('/sign/in/')
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
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'code': code
        })
        try:
            access_token_response = requests.post(ACCESS_URL,
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
        
        # 获取、存储或更新用户信息
        try:
            user_object = User.get(User.uuid == github_user_id)
            update_session(user_object)
            return redirect(url_for('home.index'))
        except DoesNotExist:
            user_object = User(uuid=github_user_id, name=name,
                               avatar_url=avatar_url, email=email)
            user_object.save()
            update_session(user_object)
            return redirect(url_for('home.index'))
        except Exception as e:
            logger.error(e)
            return abort(500)
    else:
        params = urlencode({'client_id': CLIENT_ID})
        return redirect(AUTHORIZE_URL + '?' + params)


@home.route('/sign/out/')
def sign_out():
    session.clear()
    return redirect(url_for('home.index'))


@home.route('/category/<input_category>/')
def category(input_category):
    """
    PaginatedQuery 会通过 GET 请求的 page 参数返回该页的内容
    """
    
    menu_url = quote(request.path.encode('utf-8'))
    contents = Content.select(Category, Content)\
                      .join(Category)\
                      .where(Category.name == input_category,
                             Content.status == 1)
    # 分页
    page_object = PaginatedQuery(contents,
                                 paginate_by=PAGE_MAX,
                                 check_bounds=True)
    page_count = page_object.get_page_count()
    current_page = page_object.get_page()
    projects = page_object.get_object_list()

    for project in projects:
        collected, collected_project_id = get_collected_project_status(
            project.project_url)
        if collected:
            project.collected = collected
            project.collected_project_id = collected_project_id

        project.description = markdown2html(project.description)
        project.image_url = make_image_url(project.image_path)
    return render_template('home/category.html', projects=projects,
                           menu_url=menu_url, page_title=input_category,
                           category_url=quote(input_category.encode('utf-8')),
                           page_count=page_count, current_page=current_page)


@home.route('/volume/<input_volume>/')
def volume(input_volume):
    menu_url = quote(request.path.encode('utf-8'))

    content_objects = Content.select(Content, Volume) \
                             .join(Volume) \
                             .where(Volume.name == input_volume,
                                    Volume.status == 1,
                                    Content.status == 1)

    categories = Category.select().order_by(Category.name)
    
    volumes = Volume.select()\
                    .where(Volume.status == 1)\
                    .order_by(Volume.name.asc())
    volume_name_list = [fi_volume_obj.name for fi_volume_obj in volumes]
    if input_volume in volume_name_list:
        current_volume_index = volume_name_list.index(input_volume)
    else:
        current_volume_index = -1
    
    contents = []
    index_num = 0
    for category_object in categories:
        projects = [category_object.name]  # 类别放在list第一个
        for fi_content in content_objects:
            if fi_content.category.name == category_object.name:
                collected, collected_project_id = get_collected_project_status(
                    fi_content.project_url)
                if collected:
                    fi_content.collected = collected
                    fi_content.collected_project_id = collected_project_id
                index_num += 1
                fi_content.index_num = index_num
                fi_content.description = markdown2html(fi_content.description)
                fi_content.image_url = make_image_url(fi_content.image_path)
                projects.append(fi_content)
        if not len(projects) == 1:
            contents.append(projects)
    return render_template('home/volume.html', contents=contents,
                           menu_url=menu_url,
                           volume_name_list=volume_name_list,
                           current_volume_index=current_volume_index,
                           page_title=u'第 {vol} 期'.format(vol=input_volume))


@home.route('/about/')
def about():
    content_menu_url = quote(request.args.get('url', '/').encode('utf-8'))
    return render_template('home/about.html', page_title=u'关于',
                           menu_url=content_menu_url)

@home.route('/tiobe/')
@home.route('/tiobe/<int:year>/<int:month>')
def tiobe_index(year=None, month=None):
    content_menu_url = quote(request.args.get('url', '/').encode('utf-8'))
    try:
        if year and month:
            content = TiobeContent.select()\
                                  .where(TiobeContent.publish_date.month==month,
                                         TiobeContent.publish_date.year==year)\
                                  .get()
        else:
            content = TiobeContent.select() \
                                  .order_by(TiobeContent.publish_date.desc()) \
                                  .get()
    except DoesNotExist:
        abort(404)
    # variation: 当月数据对比上月 rank 数据的变化
    ranks = TiobeRank.raw("""select r2.language, r2.position, r2.rating ,r2.rating_int - r1.rating_int as variation from
                            (select * from tioberank where MONTH(publish_date)=%s and YEAR(publish_date)=%s) as r1
                            right outer join (select * from tioberank where MONTH(publish_date)=%s and YEAR(publish_date)=%s) as r2
                            on r1.language=r2.language;""", content.publish_date.month-1, content.publish_date.year, content.publish_date.month, content.publish_date.year)

    halls = TiobeHall.select().where(TiobeHall.publish_date.month == content.publish_date.month,
                                     TiobeHall.publish_date.year == content.publish_date.year)
    
    for rank in ranks:
        for hall in halls:
            if rank.language == hall.language:
                # 某个语言多次成为明星语言，年份通过'逗号'隔开
                if hasattr(rank, 'star'):
                    rank.star = str(rank.star)+', '+str(hall.year)
                else:
                    rank.star = hall.year

    page_title = content.publish_date.strftime('%Y年%m月').decode('utf-8') + u'编程语言排行榜'
    
    return render_template('home/tiobe.html', content=content,
                           ranks=ranks, menu_url=content_menu_url,
                           page_title=page_title)
