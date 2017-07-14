# hellogithub.com
<p align="center">
  <img src="https://github.com/521xueweihan/hellogithub.com/blob/master/hellogithub.gif">
</p>

## 简介
本项目为 [hellogithub.com](https://hellogithub.com) 网站的源码。

既然做的是开源的项目推荐，那么索性就把该网站也开源了。

同时，因为很多新手想加入到开源社区，然后不知道如何开始，接下来我会基于本项目（Flask Web开发）
编写一系列的教程，题目：**让 Python 带你走进开源的世界**

内容涵盖：
- 开源介绍
- GitHub、Git 的使用
- Web 开发（基于 Flask）
- 开源项目管理

**想法还是个雏形，欢迎讨论和提供建议**，我觉得可能需要拉个微信群，我的微信号：xueweihan（请备注 hellogithub）

## 现在
此项目基于 Flask 开发，现在只开发了一些基本功能，并没有集成 flask 的第三方库。现已发开的功能：
- OAuth 登陆
- 后台内容管理
- 前端异步展示

之所以如此简陋就选择开源。因为，我想呈现的就是**从零到一**的过程。在这个过程中，历经的开发、集成库、重构的过程和思想，
才是我想分享给大家的。通过上述的过程可以让新手更好的理解 **开源思想**、**第三方库的优劣**、**Web 开发技术**、**开发流程** 等。

## 安装
1. 下载项目：`git clone https://github.com/521xueweihan/hellogithub.com.git`
2. 安装依赖：`pip install -r requirements.txt`
3. 配置
4. 启动：`python server.py`

**配置步骤如下：**

在该目录下：`/项目地址/hellogithub.com/hellogithub/hellogithub/` 创建 `config.py`，配置内容如下：
```python
#/usr/bin/env python
# -*- coding:utf-8 -*-
from os import path

DEBUG = True
SECRET_KEY = 'test_secret_key'
STATIC_PATH = path.join(path.dirname(__file__), 'static')

PAGE_MAX = 5
GITHUB_IMAGE_URL = u'https://raw.githubusercontent.com/521xueweihan/HelloGitHub/{path}'
GITHUB_IMAGE_PREFIX = u'https://github.com/521xueweihan/HelloGitHub/blob/'
GITHUB_IMAGE_PATH_PREFIX = u'master/content/{volume_name}/img/{image_name}'

APP_DIR = '/项目地址/hellogithub.com/hellogithub'

GITHUB_TEMPLAT_PATH = path.join(APP_DIR, 'output_template/github_template.md')
GITBOOK_TEMPLAT_PATH = path.join(APP_DIR, 'output_template/gitbook_template.md')

DATABASE = 'sqliteext:///%s' % path.join(APP_DIR, 'test_hellogithub.db')


# GitHub OAuth local
CLIENT_ID = '02f1c617c1b20948b635'
CLIENT_SECRET = '2102c5c75d7482acf70a09317b697d6892380adc'
AUTHORIZE_URL = 'https://github.com/login/oauth/authorize/'
ACCESS_URL = 'https://github.com/login/oauth/access_token/'
```

**开启 admin 权限：**
- 登陆一次
- 修改数据库中 admin 字段为 1
- 注销，重新登陆
- 点击用户名即可跳转到管理后台


## Todo
坑太多了，不立 flag 还能活 😅

但有一点我可以保证：本项目也会持续的迭代。
