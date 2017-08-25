# hellogithub.com
<p align="center">
  <img src="https://github.com/521xueweihan/hellogithub.com/blob/master/hellogithub.gif">
</p>

## 简介
本项目为 [hellogithub.com](https://hellogithub.com) 网站的源码。既然做的是开源的项目推荐，那么索性就把该网站也开源了。

## 现在
此项目基于 Flask 开发，现在只开发了一些基本功能，并没有集成 flask 的第三方库。现已发开的功能：
- OAuth 登陆
- 后台内容管理
- 前端异步展示
- 我的收藏
- 基本的安全防范

之所以如此简陋就选择开源。因为，我想呈现的就是**从零到一**的过程。在这个过程中，历经的开发、集成库、重构的过程和思想，
才是我想分享给大家的。通过上述的过程可以让新手更好的理解 **开源思想**、**第三方库的优劣**、**Web 开发技术**、**开发流程** 等。

## 安装
1. 下载项目：`git clone https://github.com/521xueweihan/hellogithub.com.git`
2. 安装依赖：`pip install -r requirements.txt`
3. 启动：`python server.py`

**开启 admin 权限：**
- 登陆一次
- 修改数据库中 admin 字段为 1
- 注销，重新登陆
- 点击用户名即可跳转到管理后台


## Todo
- 信息流（保证每天有内容产出）
- 订阅

有一点我可以保证：本项目也会持续的迭代。
