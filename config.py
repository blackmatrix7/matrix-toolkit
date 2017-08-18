#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/8/18 上午9:31
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : config.py
# @Software: PyCharm

__author__ = 'blackmatrix'


class ConfigMixin:

    def __setitem__(self, key, value):
        raise AttributeError

    def __delitem__(self, key):
        raise AttributeError

    def __getitem__(self, item):
        return getattr(self, item)

    def __iter__(self):
        yield from {k: getattr(self, k, None) for k in dir(self) if k.upper() == k}.items()

    def items(self):
        return self

    def get(self, item, value=None):
        return getattr(self, item, value)


class BaseConfig(ConfigMixin):
    pass


class DefaultConfig(BaseConfig):

    # Cache
    CACHE_MEMCACHED_SERVERS = ['127.0.0.1:11211']
    CACHE_KEY_PREFIX = 'default'


default = DefaultConfig()

configs = {'default': default}

config_name = 'default'
try:
    import localconfig
    current_config = localconfig.configs[config_name]
except ImportError:
    current_config = configs[config_name]
