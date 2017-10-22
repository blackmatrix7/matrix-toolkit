#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2017/9/27 下午10:48
# @Author: BlackMatrix
# @Site: https://github.com/blackmatrix7
# @File: handler
# @Software: PyCharm
import json
from tornado import web
from .session import scope, db

__author__ = 'blackmatrix'


class BaseHandler(web.RequestHandler):

    def __init__(self, application, request, **kwargs):
        self._arguments = None
        self._content_type = None
        super().__init__(application, request, **kwargs)

    @property
    def arguments(self):
        if self._arguments:
            return self._arguments
        else:
            self._arguments = {key: self.get_argument(key) for key in self.request.arguments}
            return self._arguments

    @property
    def body_arguments(self):
        try:
            body_args = json.loads(self.request.body.decode())
            return body_args
        except (ValueError, TypeError):
            return {}

    @property
    def content_type(self):
        if self._content_type:
            return self._content_type
        else:
            self._content_type = self.request.headers['Content-Type'].lower() if 'Content-Type' in self.request.headers else None
            return self._content_type

    def prepare(self):
        scope.set(self)

    def on_finish(self):
        scope.set(self)
        db.remove()
        scope.set(None)

    # make pycharm happy
    def data_received(self, chunk):
        raise NotImplementedError()

if __name__ == '__main__':
    pass
