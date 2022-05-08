#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   2022-05-07 19:20
#   Desc    :
from os import path
from flask import Flask, render_template

app = Flask(__name__)
project_path = path.dirname(__file__)

config = {
    'DEBUG': True,
    'STATIC_PATH': path.join(project_path, 'static'),
}
app.config.from_mapping(config)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
