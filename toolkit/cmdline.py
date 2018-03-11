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
        self._config = None
        self._command = sys.argv[2] if len(sys.argv) >= 3 else 'runserver'
        self._django_cmds = None

    @property
    def main(self):
        return self._main

    @property
    def config(self):
        if self._config is not None:
            return self._config
        else:
            for argv in sys.argv:
                if 'env=' in argv or 'e=' in argv:
                    config = sys.argv[1][sys.argv[1].find('=') + 1:]
                    sys.argv.remove(argv)
                    return config
            else:
                return 'debug'

    @property
    def command(self):
        assert self.config
        try:
            import django
            return sys.argv
        except ImportError:
            if sys.platform == 'win32':
                self._command = sys.argv[2] if len(sys.argv) >= 3 else 'runserver'
            else:
                self._command = sys.argv[1] if len(sys.argv) >= 2 else 'runserver'

    @property
    def settings(self):
        settings_folder = 'local_settings'
        try:
            import local_settings
        except ImportError:
            settings_folder = 'settings'
        return '{}.{}'.format(settings_folder, self.config)


cmdline = CmdLine()
