#!/usr/bin/env python
# -*- coding:utf-8 -*-
#   
#   Author  :   XueWeiHan
#   Date    :   17/6/14 下午10:50
#   Desc    :   生成输出内容
import os

from hellogithub.models import Category, Volume, Content
from hellogithub import database, app

CONTENT_FLAG = '{{ hello_github_content }}'
NUM_FLAG = '{{ hello_github_num }}'

CATEGORY_TEMPLE = u"#### {category}\n"
PROJECT_TEMPLE = u"{index_num}、[{title}]({project_url})：{description}"


def read_file(input_path):
    input_path = os.path.normpath(input_path)
    with open(input_path, 'r') as fb:
        return fb.read()


def read_from_db(volume_id):
    with database.execution_context():
        volume_object = Volume.select().where(Volume.id == volume_id).get()
        category_objects = Category.select().order_by(Category.name)
        content_objects = Content.select().where(Content.volume == volume_object)
    
        contents = []
        index_num = 0
        for category in category_objects:
            projects = [category.name]  # 类别放在list第一个
            for fi_content in content_objects:
                if fi_content.category.name == category.name:
                    index_num += 1
                    project_dict = {
                        'index_num': index_num,
                        'title': fi_content.title,
                        'description': fi_content.description,
                        'image_path': fi_content.image_path,
                        'project_url': fi_content.project_url,
                    }
                    projects.append(project_dict)
            if not len(projects) == 1:
                contents.append(projects)
    # contents 内容如下
    # [[catgory_name, project_info_dict1, project_info_dict2],...]
    return volume_object.name.encode('utf-8'), contents

            
def generate_image_url(image_path, volume_num, output_type):
    if not image_path:
        return ''
    if output_type == 'gitbook':
        image_url_format = '/volume{vol_num}/img/'.format(vol_num=volume_num)
        image_url = image_url_format+image_path.split('/')[-1]
    elif output_type == 'github':
        image_url = app.config['GITHUB_IMAGE_PREFIX']+image_path
    else:
        return ''
    return u"![]({image_url})\n\n".format(image_url=image_url)


def volume_name2volume_id(volume_name):
    with database.execution_context():
        volume_object = Volume.select().where(Volume.name == volume_name).get()
    return volume_object.id


def generate_markdown(volume_id, output_type):
    content_str = u""""""
    volume_num, content_list = read_from_db(volume_id)
    
    for project_list in content_list:
        category = project_list.pop(0)
        content_str += CATEGORY_TEMPLE.format(category=category)
        for project in project_list:
            if not project['description'].endswith('\n\n'):
                project['description'] += u'\n'
            content_str += PROJECT_TEMPLE.format(**project)
            content_str += generate_image_url(
                project['image_path'], volume_num, output_type)
    if output_type == 'github':
        temple_data = read_file(app.config['GITHUB_TEMPLAT_PATH'])
        temple_data = temple_data.replace(NUM_FLAG, volume_num)
    elif output_type == 'gitbook':
        temple_data = read_file(app.config['GITBOOK_TEMPLAT_PATH'])
        temple_data = temple_data.replace(NUM_FLAG, volume_num)
    else:
        return ''
    content_str = content_str.encode('utf-8')
    output_str = temple_data.replace(CONTENT_FLAG, content_str)
    return output_str
