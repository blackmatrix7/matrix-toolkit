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
        from copy import copy
        argv = copy(sys.argv)
        del argv[1]
        return argv

cmdline = CmdLine()