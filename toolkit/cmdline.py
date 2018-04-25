#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/8/4 上午11:19
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : cmdline.py
# @Software: PyCharm
import sys
from importlib import import_module

__author__ = 'blackmatrix'


class CmdLine:

    def __init__(self):
        self._main = sys.argv[0]
        self._config = None
        self._command = sys.argv[2] if len(sys.argv) >= 3 else 'runserver'
        self._django_cmds = None
        self._settings = None

    @property
    def main(self):
        return self._main

    def get_config(self):
        if self._config is not None:
            return self._config
        else:
            for argv in sys.argv:
                # 兼容django自带的settings参数
                if 'settings=' in argv.lower():
                    self._settings = argv[argv.find('=') + 1:]
                    return self._settings
                # flask、tornado 使用cfg参数
                # django 也可以使用cfg参数
                elif 'cfg=' in argv.lower():
                    self._config = argv[argv.find('=') + 1:]
                    sys.argv.remove(argv)
                    return self._config
            else:
                return 'default'

    @property
    def config(self):
        return self._config or self.get_config()

    @property
    def command(self):
        assert self.config
        try:
            # django 下原样返回
            import django
            return sys.argv
        except ImportError:
            if sys.platform == 'win32':
                self._command = sys.argv[2] if len(sys.argv) >= 3 else 'runserver'
            else:
                self._command = sys.argv[1] if len(sys.argv) >= 2 else 'runserver'

    @property
    def settings(self):
        # 获取配置文件名
        self.get_config()
        # django的--settings参数直接返回，不支持本地配置文件
        if self._settings:
            return self._settings
        else:
            settings_folder = 'local_settings'
            try:
                import_module('local_settings.{config}'.format(config=self.config))
            except ImportError:
                settings_folder = 'settings'
            return '{}.{}'.format(settings_folder, self.config)


cmdline = CmdLine()
