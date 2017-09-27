#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/8/18 上午9:31
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : config.py
# @Software: PyCharm
from toolkit import BaseConfig, get_current_config

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

    # RabbitMQ
    RABBITMQ_HOST = '127.0.0.1'
    RABBITMQ_PORT = 5672
    RABBITMQ_USER = 'user'
    RABBITMQ_PASS = 'password'


"""
以下为测试用数据
"""


class BaseDemoConfig(BaseConfig):

    # HOST
    HOST = '127.0.0.1'

    """
    对于需要通过其他属性运算获得的属性参数，需要定义在特性中
    """
    LOGIN_URL = property(lambda self: 'http://{host}/login'.format(host=self.HOST))


class DemoConfig01(BaseDemoConfig):
    # HOST
    HOST = '192.168.1.10'


class DemoConfig02(BaseDemoConfig):
    # HOST
    HOST = '10.10.10.10'


default = DefaultConfig()
demo01 = DemoConfig01()
demo02 = DemoConfig02()


configs = {'default': default,
           'demo01': demo01,
           'demo02': demo02}

# 读取配置文件的名称，在具体的应用中，可以从环境变量、命令行参数等位置获取配置文件名称
config_name = 'default'

current_config = get_current_config(config_name)
