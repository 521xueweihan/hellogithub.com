#!/usr/bin/env python
# -*- coding:utf-8 -*-
#   
#   Author  :   XueWeiHan
#   Date    :   17/8/30 下午4:47
#   Desc    :
from huey import crontab

from config import huey, tiobe_config
from tiobe_spider import Tiobe


@huey.periodic_task(crontab(minute='*/120'))
def tiobe_spider():
    t = Tiobe(tiobe_config['rss_url'], tiobe_config['index_url'])
    t.fetch()
