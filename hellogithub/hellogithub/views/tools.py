#!/usr/bin/env python
# -*- coding:utf-8 -*-
#   
#   Author  :   XueWeiHan
#   Date    :   17/6/12 下午12:19
#   Desc    :   工具函数
import markdown2
from playhouse.shortcuts import model_to_dict

from ..config import GITHUB_IMAGE_PATH_PREFIX, GITHUB_IMAGE_URL, \
    GITHUB_IMAGE_PREFIX


def markdown2html(markdown_data):
    extras = ['tables', 'fenced-code-blocks', 'cuddled-lists']
    html_output = markdown2.markdown(
        markdown_data,
        safe_mode=True,
        extras=extras,
    ).replace('<p>', '').replace('</p>', '')
    return html_output


def models_to_dicts(query_models):
    dict_list = []
    for query_model in query_models:
        dict_list.append(model_to_dict(query_model))
    return dict_list


def make_description(description):
    if not description.endswith('\n'):
        description += '\n'
    return description


def make_image_path(volume_name, image_name):
    if not image_name:
        return ''
    return GITHUB_IMAGE_PATH_PREFIX.format(volume_name=volume_name,
                                           image_name=image_name)


def get_image_name(image_path):
    if image_path:
        image_name = image_path.split('/')[-1]
        return image_name
    else:
        return ''


def make_image_url(image_path):
    """
    生成 image_url
    """
    if image_path:
        return GITHUB_IMAGE_URL.format(path=image_path)
    else:
        return image_path


def generate_out_url(image_path):
    """
    生成用于输出 markdown 的 image_url
    """
    if image_path:
        return GITHUB_IMAGE_PREFIX+image_path
    else:
        return image_path
