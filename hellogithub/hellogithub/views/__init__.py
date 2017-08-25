#!/usr/bin/env python
# -*- coding:utf-8 -*-
#   
#   Author  :   XueWeiHan
#   Date    :   17/6/12 上午10:48
#   Desc    :   View 层


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class InvalidParams(InvalidUsage):
    def __init__(self, message=u'参数错误'):
        super(InvalidParams, self).__init__(message)


class ParamsConflict(InvalidUsage):
    def __init__(self, message=u'已存在', status_code=409):
        super(ParamsConflict, self).__init__(message, status_code)


class Unauthorized(InvalidUsage):
    def __init__(self, message=u'需要登录', status_code=401):
        super(Unauthorized, self).__init__(message, status_code)