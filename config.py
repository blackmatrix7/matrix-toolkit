#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/8/18 上午9:31
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : config.py
# @Software: PyCharm
from tookit import BaseConfig, get_current_config

__author__ = 'blackmatrix'


class DefaultConfig(BaseConfig):

    """
    配置文件的具体实现，所有的配置项都必须是全部大写
    """

    # DEBUG
    DEBUG = False

    # Cache
    CACHE_MEMCACHED_SERVERS = ['127.0.0.1:11211']
    CACHE_KEY_PREFIX = ''


default = DefaultConfig()

configs = {'default': default}

# 读取配置文件的名称，在具体的应用中，可以从环境变量、命令行参数等位置获取配置文件名称
config_name = 'default'

current_config = get_current_config(config_name)
