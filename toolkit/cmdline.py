#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/8/4 上午11:19
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : cmdline.py
# @Software: PyCharm
import sys

__author__ = 'blackmatrix'


class CmdLine:

    def __init__(self):
        self._main = sys.argv[0]
        self._config = sys.argv[1] if len(sys.argv) >= 2 else 'default'
        self._command = sys.argv[2] if len(sys.argv) >= 3 else 'runserver'
        self._django_cmds = None

    @property
    def main(self):
        return self._main

    @property
    def config(self):
        return self._config

    @property
    def command(self):
        return self._command

    @property
    def django_cmds(self):
        if self._django_cmds:
            return self._django_cmds
        else:
            from copy import copy
            argv = copy(sys.argv)
            del argv[1]
            self._django_cmds = argv
            return self._django_cmds

cmdline = CmdLine()
