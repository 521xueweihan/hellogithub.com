#/usr/bin/env python
# -*- coding:utf-8 -*-
#   
#   Author  :   XueWeiHan
#   Date    :   17/3/12 上午11:23
#   Desc    :   配置文件
from os import path
from logging.handlers import RotatingFileHandler
from logging import getLogger, Formatter, INFO


def setting_logger(name):
    handler = RotatingFileHandler('%s.log' % name, maxBytes=10000000, backupCount=3)
    log_object = getLogger(name)
    formatter = Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    log_object.setLevel(INFO)
    log_object.addHandler(handler)
    return log_object

flask_config = {
    'DEBUG': True,
    'SECRET_KEY': '23-04912=sda',
    'STATIC_PATH': path.join(path.dirname(__file__), 'static')
}

APP_NAME = 'hellogithub'
APP_DIR = path.dirname(path.dirname(__file__))
logger = setting_logger(APP_NAME)
DATABASE_URL = 'sqliteext:///%s' % path.join(APP_DIR, 'test_hellogithub.db')


PAGE_MAX = 5
GITHUB_IMAGE_URL = u'https://raw.githubusercontent.com/521xueweihan/HelloGitHub/{path}'
GITHUB_IMAGE_PREFIX = u'https://github.com/521xueweihan/HelloGitHub/blob/'
GITHUB_IMAGE_PATH_PREFIX = u'master/content/{volume_name}/img/{image_name}'


GITHUB_TEMPLAT_PATH = path.join(APP_DIR, 'output_template/github_template.md')
GITBOOK_TEMPLAT_PATH = path.join(APP_DIR, 'output_template/gitbook_template.md')


# GitHub OAuth
CLIENT_ID = '02f1c617c1b20948b635'
CLIENT_SECRET = '2102c5c75d7482acf70a09317b697d6892380adc'
AUTHORIZE_URL = 'https://github.com/login/oauth/authorize/'
ACCESS_URL = 'https://github.com/login/oauth/access_token/'
