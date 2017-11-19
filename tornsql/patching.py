#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/9/28 下午1:09
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : patching.py
# @Software: PyCharm
import tornado.gen
from .session import scope

__author__ = 'blackmatrix'

original_runner_init = tornado.gen.Runner.__init__
original_runner_run = tornado.gen.Runner.run
original_runner_handle_exception = tornado.gen.Runner.handle_exception


def new_runner_init(self, *args, **kwargs):
    original_runner_init(self, *args, **kwargs)
    self.scope = scope.get()


def new_runner_run(self):
    scope.set(self.scope)
    return original_runner_run(self)


def monkey_patching():
    tornado.gen.Runner.__init__ = new_runner_init
    tornado.gen.Runner.run = new_runner_run


if __name__ == '__main__':
    pass
