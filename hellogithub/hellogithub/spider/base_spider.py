#!/usr/bin/env python
# -*- coding:utf-8 -*-
#   
#   Author  :   XueWeiHan
#   Date    :   17/8/30 下午5:58
#   Desc    :   base spider
import os
import logging

import requests


class BaseSpider(object):
    spider_name = 'base'
    
    def __init__(self):
        self.logger = logging.getLogger(self.spider_name)  # 设置log名称
    
    def get_data(self, url):
        try:
            response = requests.get(url, timeout=20, verify=False)
            return response
        except Exception as e:
            self.logger.error(u"获取 {url} 数据失败：{e}".format(url=url, e=e))
            return None
