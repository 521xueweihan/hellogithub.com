# hellogithub.com
<p align="center">
  <img src="https://github.com/521xueweihan/hellogithub.com/blob/master/hellogithub.gif">
</p>

## 简介
本项目为 [hellogithub.com](https://hellogithub.com) 网站的源码。既然做的是开源的项目推荐，那么索性就把该网站也开源了。

## 现在
此项目基于 Flask 开发，现在只开发了一些基本功能。现已发开的功能，[开发日志](https://github.com/521xueweihan/hellogithub.com/blob/master/%E5%BC%80%E5%8F%91%E6%97%A5%E5%BF%97.md)：
- OAuth 登陆
- 后台内容管理
- 前端异步展示
- 我的收藏
- 基本的安全防范
- Tiobe 编程语言排名

之所以如此简陋就选择开源。因为，我想呈现的就是**从零到一**的过程。在这个过程中，历经的开发、集成库、重构的过程和思想，
才是我想分享给大家的。通过上述的过程可以让新手更好的理解 **开源思想**、**第三方库的优劣**、**Web 开发技术**、**开发流程** 等。

## 安装
### 下载项目
```bash
$ git clone https://github.com/521xueweihan/hellogithub.com.git
# 进入项目目录
$ cd hellogithub.com
```
### 创建并激活虚拟环境
为了不和本地的环境冲突，推荐使用虚拟环境, 如果不想用虚拟环境也可以跳过，但是请保证当前是Python2.7环境
```bash
# Anaconda(推荐)
$ conda create -y -n hellogithub python=2.7
# 激活环境
$ conda activate hellogithub
```
请将`/usr/bin/python2.7`替换成自己可以执行的python2.7执行路径
```bash
# virtualenv
# 如果没有可以先安装
$ pip install virtualenv
$ virtualenv -p /usr/bin/python2.7 hellogithub
# 以防万一赋予可执行权限
$ chmod +x ./hellogithub/bin/activate
# 激活环境
$ source ./hellogithub/bin/activate
```
### 安装依赖
```bash
$ pip install -r requirements.txt
```
### 启动服务
```bash
$ python hellogithub/server.py
```
启动成功后就能访问 http://127.0.0.1:4000 了
### 开启管理后台权限
- 登陆一次
- 修改数据库中 admin 字段为 1
- 注销，重新登陆
- 点击用户名即可跳转到管理后台

### 退出虚拟环境
```bash
# conda
$ conda deactivate
```
```bash
# virtualenv
$ deactivate
```

## Todo
- 已完成爬虫架子、GitHub spider，准备做view层、event信息流
- 信息流（保证每天有内容产出）
- 订阅
- 测试和CI
- 重构 API 使其符合 RESTful 风格

有一点我可以保证：本项目会一直维护下去。
