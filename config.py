#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/8/18 上午9:31
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : config.py
# @Software: PyCharm
from toolkit.config import BaseConfig, get_current_config

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


# 读取当前配置项
# current_config会根据当前的config_name获取到匹配的配置文件对象
# 如果项目根目录存在localconfig.py，则优先从localconfig.py中读取
from config import current_config
# 获取配置文件中的属性
# 配置文件对象，支持以.（点号）运算符获取对象的属性，也支持以key的形式获取对象的属性
# 以下两种方式都能获取的配置项
RABBITMQ_HOST = current_config.RABBIT_HOST
RABBITMQ_PORT = current_config['RABBITMQ_PORT']
# 配置文件支持遍历
keys = [key for key in current_config]
assert isinstance(keys, list)
values = {k: v for k, v in current_config.items()}
assert isinstance(values, dict)
