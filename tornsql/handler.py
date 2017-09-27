#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2017/9/27 下午10:48
# @Author: BlackMatrix
# @Site: https://github.com/blackmatrix7
# @File: handler
# @Software: PyCharm
from tornado import web
from .session import scope, db

__author__ = 'blackmatrix'


class BaseHandler(web.RequestHandler):

    def prepare(self):
        scope.set(self)

    def on_finish(self):
        scope.set(self)
        db.remove()
        scope.set(None)


if __name__ == '__main__':
    pass
